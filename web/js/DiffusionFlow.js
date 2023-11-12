import { SocketHandler } from './SocketHandler.js';
import { ApiService } from "./ApiService.js";

class DiffusionFlow
{
    constructor() {
        this._node_data = [];

        this._selected_nodes = [];
        this._temporary_connection = null;
        this._selected_pin = null;

        this._graph = null;

        /* region context menu stuff */

        this._context_menu = null;
        this._context_menu_visible = false;
        this._context_menu_position = {x: 0, y: 0};
        this._context_menu_position_graph_relative = {x: 0, y: 0};

        /* endregion */

        this._initialized = false;
        this._socket = new SocketHandler();
        this._api = new ApiService();

        this._socket._ws.onopen = (event) => {
            if (this._initialized) {
                return;
            }

            this.prepare_ui();
            this._initialized = true;
        };
    }

    prepare_ui() {
        this._context_menu = document.getElementById("context-menu");
        this._api.getNodes().then((nodes) => {
            this._node_data = nodes;
            this.build_context_menu();
        });

        document.addEventListener("mouseup", (event) => {
            event.preventDefault();
            if (this._selected_pin == null) {
                return;
            }

            this._selected_pin.classList.remove("pin-selected");
            let element_under_cursor = document.elementFromPoint(event.clientX, event.clientY);
            if (element_under_cursor.classList.contains("pin")) {
                this.connect_pins(this._selected_pin, element_under_cursor);
            }

            this._selected_pin = null;
        });

        [...document.getElementsByClassName("graph")].forEach((graph) => {
            this._graph = graph;

            graph.addEventListener("contextmenu", (event) => {
                event.preventDefault();
                this.show_context_menu(event.x, event.y);
                this._context_menu_position_graph_relative = {x: event.offsetX, y: event.offsetY};
            });

            graph.addEventListener("click", (event) => {
                event.preventDefault();
                if (this._context_menu_visible) {
                    this.hide_context_menu();
                }
            });
        });
    }

    build_context_menu() {
        this._context_menu.innerHTML = "";
        this._node_data.forEach((node) => {
            let item = document.createElement("div");
            item.classList.add("item");
            item.innerHTML = node.name;

            item.addEventListener("click", (event) => {
                event.preventDefault();
                let node_template = document.getElementById("node-template").cloneNode(true);
                node_template.getElementsByClassName("title")[0].innerHTML = node.name;
                node_template.style.left = this._context_menu_position_graph_relative.x + "px";
                node_template.style.top = this._context_menu_position_graph_relative.y + "px";
                node_template.id = "node-" + node.id;

                const node_unique_id = this.uuidv4();
                node_template.dataset.uniqueId = node_unique_id;
                node_template.dataset.id = node.id;

                let input_pin_template = document.getElementById("input-pin-template").cloneNode(true);
                let output_pin_template = document.getElementById("output-pin-template").cloneNode(true);

                let input_pins = node_template.getElementsByClassName("left-pins")[0];
                let output_pins = node_template.getElementsByClassName("right-pins")[0];

                node.inPins.forEach((pin) => {
                    let pin_template = input_pin_template.cloneNode(true);
                    pin_template.id = node_template.id + "-pin-" + pin.id;
                    pin_template.getElementsByClassName("pin-title")[0].innerHTML = pin.name;
                    if (pin.id.includes("exec")) {
                        pin_template.classList.add("pin-exec");
                    } else {
                        pin_template.classList.add("pin-input");
                    }

                    pin_template.dataset.pinId = pin.id;
                    pin_template.dataset.nodeUniqueId = node_unique_id;

                    input_pins.appendChild(pin_template);
                    this.bind_pin_events(pin_template);
                });

                node.outPins.forEach((pin) => {
                    let pin_template = output_pin_template.cloneNode(true);
                    pin_template.id = node_template.id + "-pin-" + pin.id;
                    pin_template.getElementsByClassName("pin-title")[0].innerHTML = pin.name;
                    if (pin.id.includes("exec")) {
                        pin_template.classList.add("pin-exec");
                    } else {
                        pin_template.classList.add("pin-input");
                    }

                    pin_template.dataset.pinId = pin.id;
                    pin_template.dataset.nodeUniqueId = node_unique_id;

                    output_pins.appendChild(pin_template);
                    this.bind_pin_events(pin_template);
                });


                this._graph.appendChild(node_template);

                this.hide_context_menu();
            });

            this._context_menu.appendChild(item);
        });
    }

    show_context_menu(mouse_x, mouse_y) {
        this._context_menu.style.display = "block";
        this._context_menu.style.left = mouse_x + "px";
        this._context_menu.style.top = mouse_y + "px";
        this._context_menu_visible = true;
        this._context_menu_position = {x: mouse_x, y: mouse_y};
    }

    hide_context_menu() {
        this._context_menu.style.display = "none";
        this._context_menu_visible = false;
    }

    bind_pin_events(pin) {
        pin.addEventListener("mousedown", (event) => {
            event.preventDefault();
            pin.classList.add("pin-selected");
            this._selected_pin = pin;
        });
    }

    connect_pins(pin_a, pin_b) {
        pin_a.dataset.connectedToNode = pin_b.dataset.nodeUniqueId;
        pin_a.dataset.connectedToPin = pin_b.dataset.pinId;
        pin_b.dataset.connectedToNode = pin_a.dataset.nodeUniqueId;
        pin_b.dataset.connectedToPin = pin_a.dataset.pinId;
    }

    uuidv4() {
      return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
      );
    }
}

window.diffusion_flow = new DiffusionFlow();