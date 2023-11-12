import { Node } from "./Node.js";

export class Graph
{
    /** @type {Editor} */
    #editor;

    /** @type {HTMLElement} */
    #element;

    /** @type {Node[]} */
    #nodes = [];

    /** @type {HTMLElement} */
    #temporaryConnection = null;

    /** @type {number} */
    #scale = 1;

    /** @type {{x: number, y: number}} */
    #viewPosition = { x: -5000, y: -5000 };

    /**
     *
     * @param {Editor} editor
     * @param {HTMLElement} element
     */
    constructor(editor, element) {
        this.#editor = editor;
        this.#element = element;

        this.#setupEvents();
    }

    /**
     *
     * @param {NodeData} nodeData
     * @param {number} x
     * @param {number} y
     * @returns {Node}
     */
    addNode(nodeData, x, y) {
        const node = Node.build(this, nodeData);
        this.#nodes.push(node);

        this.moveNode(node, x, y);
        this.#element.appendChild(node.element);

        return node;
    }

    /**
     *
     * @param {Pin} pin
     * @param {NodeData} nodeData
     * @param {number} x
     * @param {number} y
     * @returns {Node}
     */
    addNodeFromPin(pin, nodeData, x, y) {
        const node = this.addNode(nodeData, x, y);
        const matchingPin = node.findMatchingInputPin(pin);
        if (matchingPin === null) {
            return node;
        }

        matchingPin.connectTo(pin);
        return node;
    }

    moveNode(node, x, y) {
        node.move(x, y);
    }

    /**
     *
     * @param {HTMLElement} element
     * @returns {Pin|null}
     */
    findPinByHTMLElement(element) {
        const nodeUniqueId = element.dataset.nodeUniqueId;
        const pinId = element.dataset.pinId;

        const node = this.#nodes.find((node) => {
            return node.uniqueId === nodeUniqueId;
        });

        if (node === null || node === undefined) {
            return null;
        }

        return node.findPin(pinId);
    }

    toJson() {
        return {
            nodes: this.#nodes.map((node) => {
                return node.toJson();
            }),
            connections: this.#nodes.flatMap((node) => {
                return node.toJsonConnections();
            }),
        };
    }

    #setupEvents() {
        this.#element.addEventListener("contextmenu", (event) => {
            event.preventDefault();
            this.#editor.contextMenu.showAt(this, event.clientX, event.clientY, {
                x: event.offsetX,
                y: event.offsetY,
            });
            event.stopPropagation();
        });

        this.#element.addEventListener("mousedown", (event) => {
            const onMouseMove = (event) => {
                event.preventDefault();
                event.stopPropagation();

                this.#viewPosition.x += event.movementX / this.scale;
                /*const limitX = -250 / this.scale, limitY = -30 / this.scale;
                if (this.#viewPosition.x > limitX) {
                    this.#viewPosition.x = limitX;
                }*/

                this.#viewPosition.y += event.movementY / this.scale;
                /*if (this.#viewPosition.y > limitY) {
                    this.#viewPosition.y = limitY;
                }*/

                this.#element.style.transform = `scale(${this.#scale}) translate(${this.#viewPosition.x}px, ${this.#viewPosition.y}px)`;
            };

            this.#element.addEventListener("mousemove", onMouseMove);
            this.#element.addEventListener("mouseup", (event) => {
                event.preventDefault();
                event.stopPropagation();

                this.#element.removeEventListener("mousemove", onMouseMove);
            }, { once: true });
        });

        this.#element.addEventListener("mousemove", (event) => {
            //console.log(event.pageX);
            //this.#element.style.transformOrigin = `${event.clientX}px ${event.clientY}px`;
        });

        this.#element.addEventListener("wheel", (event) => {
            event.preventDefault();
            event.stopPropagation();

            if (event.deltaY > 0) {
                if (this.#scale >= 0.5) {
                    this.#scale -= 0.1;
                }
            } else {
                if (this.#scale <= 1.5) {
                    this.#scale += 0.1;
                }
            }

            // this.#element.style.transformOrigin = `${event.clientX}px ${event.clientY}px`;
            this.#element.style.transformOrigin = "0 0";
            this.#element.style.transform = `scale(${this.#scale}) translate(${this.#viewPosition.x}px, ${this.#viewPosition.y}px)`;
        });

        document.querySelector("#quick-menu a#upload-graph").addEventListener("click", (event) => {
            this.#editor.apiService.executeGraph(this);
        });
    }

    /**
     *
     * @returns {HTMLElement}
     */
    get element() {
        return this.#element;
    }

    /**
     *
     * @returns {number}
     */
    get scale() {
        return this.#scale;
    }
}