import asyncio
import mimetypes
import os
import struct
import uuid
from asyncio import AbstractEventLoop
from io import BytesIO
from PIL import Image, ImageOps

import aiohttp
from aiohttp import web

import mapping
from bluepynt import Bluepynt

routes = web.RouteTableDef()


class BinaryEventTypes:
    PREVIEW_IMAGE = 1
    UNENCODED_PREVIEW_IMAGE = 2


async def send_socket_catch_exception(function, message):
    try:
        await function(message)
    except (aiohttp.ClientError, aiohttp.ClientPayloadError, ConnectionResetError) as err:
        print("send error:", err)


@web.middleware
async def cache_control(request: web.Request, handler):
    response: web.Response = await handler(request)
    if request.path.endswith('.js') or request.path.endswith('.css'):
        response.headers.setdefault('Cache-Control', 'no-cache')
    return response


class WebServer:
    def __init__(self, loop: AbstractEventLoop):
        mimetypes.init()
        mimetypes.types_map['.js'] = 'application/javascript; charset=utf-8'

        middlewares = [cache_control]

        self.sockets: dict = {}
        self.messages = asyncio.Queue()
        self.loop = loop
        self.app = web.Application(client_max_size=1024**3, middlewares=middlewares)
        self.web_root = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "web")

        self.routes = routes
        self.last_node_id = None
        self.client_id = None

        @routes.get('/ws')
        async def websocket_handler(request):
            ws = web.WebSocketResponse()
            await ws.prepare(request)
            sid = request.rel_url.query.get('clientId', '')
            if sid:
                self.sockets.pop(sid, None)
            else:
                sid = uuid.uuid4().hex

            self.sockets[sid] = ws

            try:
                await self.send("status", {"status": {}, 'sid': sid}, sid)
                if self.client_id == sid and self.last_node_id is not None:
                    await self.send("executing", {"node": self.last_node_id}, sid)

                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.ERROR:
                        print('ws connection closed with exception %s' % ws.exception())
            finally:
                self.sockets.pop(sid, None)
            return ws

        @routes.get("/")
        async def get_root(request):
            return web.FileResponse(os.path.join(self.web_root, "index.html"))

        @routes.get("/api/nodes")
        async def get_nodes(request):
            nodes = []
            for node_id in mapping.NODE_MAP:
                node = mapping.NODE_MAP[node_id]()
                nodes.append(node.to_json())
            return web.json_response(nodes)

        @routes.post("/api/execute")
        async def post_execute(request):
            data = await request.json()
            graphs = Bluepynt.load_graph_from_structure(data)
            graphs[0].execute()
            return web.json_response({})

    async def start(self, address: str = "", port: int = None):
        if port is None:
            port = 7860

        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, address, port)
        await site.start()

        if address == "":
            address = "0.0.0.0"

        print("Starting server\n")
        print(f"To see the GUI go to: http://{address}:{port}")

    async def send(self, event, data, sid=None):
        if event == BinaryEventTypes.UNENCODED_PREVIEW_IMAGE:
            await self.send_image(data, sid=sid)
        elif isinstance(data, (bytes, bytearray)):
            await self.send_bytes(event, data, sid)
        else:
            await self.send_json(event, data, sid)

    def encode_bytes(self, event, data):
        if not isinstance(event, int):
            raise RuntimeError(f"Binary event types must be integers, got {event}")

        packed = struct.pack(">I", event)
        message = bytearray(packed)
        message.extend(data)
        return message

    async def send_image(self, image_data, sid=None):
        image_type = image_data[0]
        image = image_data[1]
        max_size = image_data[2]
        if max_size is not None:
            if hasattr(Image, 'Resampling'):
                resampling = Image.Resampling.BILINEAR
            else:
                resampling = Image.ANTIALIAS

            image = ImageOps.contain(image, (max_size, max_size), resampling)
        type_num = 1
        if image_type == "JPEG":
            type_num = 1
        elif image_type == "PNG":
            type_num = 2

        bytes_io = BytesIO()
        header = struct.pack(">I", type_num)
        bytes_io.write(header)
        image.save(bytes_io, format=image_type, quality=95, compress_level=4)
        preview_bytes = bytes_io.getvalue()
        await self.send_bytes(BinaryEventTypes.PREVIEW_IMAGE, preview_bytes, sid=sid)

    async def send_bytes(self, event, data, sid=None):
        message = self.encode_bytes(event, data)

        if sid is None:
            for ws in self.sockets.values():
                await send_socket_catch_exception(ws.send_bytes, message)
        elif sid in self.sockets:
            await send_socket_catch_exception(self.sockets[sid].send_bytes, message)

    async def send_json(self, event, data, sid=None):
        message = {"type": event, "data": data}

        if sid is None:
            for ws in self.sockets.values():
                await send_socket_catch_exception(ws.send_json, message)
        elif sid in self.sockets:
            await send_socket_catch_exception(self.sockets[sid].send_json, message)

    def send_sync(self, event, data, sid=None):
        self.loop.call_soon_threadsafe(self.messages.put_nowait, (event, data, sid))

    async def publish_loop(self):
        while True:
            msg = await self.messages.get()
            await self.send(*msg)

    def add_routes(self):
        self.app.add_routes(self.routes)

        self.app.add_routes([
            web.static('/', self.web_root, follow_symlinks=True),
        ])
