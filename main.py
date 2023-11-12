import asyncio
import os
import threading

import mapping
from server import WebServer


def prompt_worker():
    pass


async def run(web_server: WebServer, address: str = "", port=8188, verbose=True):
    await asyncio.gather(server.start(address, port), server.publish_loop())


if __name__ == '__main__':
    mapping.load_nodes_from_module(os.path.join(os.path.dirname(os.path.realpath(__file__)), "src/bluepynt", "builtin",
                                                "macros.py"))
    mapping.load_nodes_from_module(os.path.join(os.path.dirname(os.path.realpath(__file__)), "src/bluepynt", "builtin",
                                                "nodes.py"))
    mapping.load_nodes_from_module(os.path.join(os.path.dirname(os.path.realpath(__file__)), "src/bluepynt", "builtin",
                                                "pure_nodes.py"))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = WebServer(loop)

    server.add_routes()

    threading.Thread(target=prompt_worker, daemon=True, args=()).start()

    call_on_start = None

    try:
        address = "0.0.0.0"
        if os.name == 'nt' and address == "0.0.0.0":
            address = "127.0.0.1"
        loop.run_until_complete(run(server, address=address, port=7860, verbose=True))
    except KeyboardInterrupt:
        print("\nStopped server")
