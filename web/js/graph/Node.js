import { NodeData } from "../api/NodeData.js";
import { UUIDv4 } from "../Utils.js";
import { Pin } from "./Pin.js";

export class Node extends EventTarget
{
    /** @type {Graph} */
    #graph;

    /** @type {HTMLElement} */
    #element;

    /** @type {string} */
    #uniqueId;

    /** @type {NodeData} */
    #data;

    /** @type {Pin[]} */
    #inPins = [];

    /** @type {Pin[]} */
    #outPins = [];

    #mouseMoveOffset = null;

    /**
     *
     * @param {Graph} graph
     * @param {Element} element
     * @param {string} uniqueId
     * @param {NodeData} nodeData
     */
    constructor(graph, element, uniqueId, nodeData) {
        super();
        this.#graph = graph;
        this.#element = element;
        this.#data = nodeData;
        this.#uniqueId = uniqueId;

        const inPinsElement = this.#element.getElementsByClassName("left-pins")[0];
        this.#inPins = this.#data.inPins.map((pinData) => {
            const pin = Pin.build(this, pinData, true);
            inPinsElement.appendChild(pin.element);
            return pin;
        });

        const outPinsElement = this.#element.getElementsByClassName("right-pins")[0];
        this.#outPins = this.#data.outPins.map((pinData) => {
            const pin = Pin.build(this, pinData, false);
            outPinsElement.appendChild(pin.element);
            return pin;
        });

        this.#setupEvents();
    }

    move(x, y) {
        this.#element.style.left = x + "px";
        this.#element.style.top = y + "px";

        this.dispatchEvent(new CustomEvent("move", {
            x: x,
            y: y
        }));

        // this.#outPins.forEach((pin) => {
        //     pin.update();
        // });
        //
        // this.#inPins.forEach((pin) => {
        //     pin.update();
        // });
    }

    moveBy(xOffset, yOffset) {
        this.move(this.position.x + xOffset, this.position.y + yOffset);
    }

    getInFlowPin(pinId) {
        return this.#inPins.find((pin) => {
            return pin.pinData.pinId === pinId && pin.isFlow;
        });
    }

    getOutFlowPin(pinId) {
        return this.#outPins.find((pin) => {
            return pin.pinData.pinId === pinId && pin.isFlow;
        });
    }

    getInArgumentPin(pinId) {
        return this.#inPins.find((pin) => {
            return pin.pinData.pinId === pinId && pin.isArgument;
        });
    }

    getOutArgumentPin(pinId) {
        return this.#outPins.find((pin) => {
            return pin.pinData.pinId === pinId && pin.isArgument;
        });
    }

    /**
     *
     * @param {Pin} pin
     * @returns {Pin}
     */
    findMatchingInputPin(pin) {
        let matchingPin = null;
        this.#inPins.every((inputPin) => {
            if (inputPin.pinData.pinType === pin.pinData.pinType) {
                if (pin.isFlow) {
                    matchingPin = inputPin;
                    return false;
                }

                // TODO: matching Any types
                if (pin.argumentType === inputPin.argumentType) {
                    matchingPin = inputPin;
                    return false;
                }
            }

            return true;
        });

        return matchingPin;
    }

    /**
     *
     * @returns {Graph}
     */
    get graph() {
        return this.#graph;
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
     * @returns {string}
     */
    get uniqueId() {
        return this.#uniqueId;
    }

    /**
     *
     * @returns {NodeData}
     */
    get data() {
        return this.#data;
    }

    get position() {
        return {
            x: parseFloat(this.#element.style.left.replace("px", "")),
            y: parseFloat(this.#element.style.top.replace("px", ""))
        };
    }

    /**
     *
     * @param {string} pinId
     * @returns {Pin|null}
     */
    findPin(pinId) {
        return this.#inPins.find((pin) => {
            return pin.pinData.pinId === pinId;
        }) ?? this.#outPins.find((pin) => {
            return pin.pinData.pinId === pinId;
        });
    }

    /**
     *
     * @param {string} pinId
     * @returns {Pin[]}
     */
    findPinsDependingOn(pinId) {
        const inPins = this.#inPins.filter((pin) => {
            return pin.pinData.typeDependsOn === pinId;
        });
        const outPins = this.#outPins.filter((pin) => {
            return pin.pinData.typeDependsOn === pinId;
        });

        return [...inPins, ...outPins];
    }


    /**
     *
     * @param graph
     * @param {NodeData} nodeData
     * @returns {Node}
     */
    static build(graph, nodeData) {
        let nodeElement = document.getElementById("node-template").cloneNode(true);
        const uniqueId = UUIDv4();

        nodeElement.id = "";
        nodeElement.getElementsByClassName("title")[0].getElementsByTagName("h5")[0].innerHTML = nodeData.name;

        nodeElement.dataset.nodeId = nodeData.nodeId;
        nodeElement.dataset.uniqueId = uniqueId;
        nodeElement.dataset.baseType = nodeData.baseType;
        if (nodeData.description !== "") {
            console.log(nodeElement);
            console.log(nodeElement.getElementsByClassName("description-tooltip")[0]);
            nodeElement.getElementsByClassName("description-tooltip")[0].dataset.description = nodeData.description;
        }

        if (nodeData.baseType === "functions") {
            nodeElement.dataset.isPure = nodeData.isPure;
        }

        return new Node(graph, nodeElement, uniqueId, nodeData);
    }

    toJson() {
        let args = {};
        this.#inPins.forEach((pin) => {
            if (pin.isFlow) {
                return;
            }

            if (pin.isConnected) {
                return;
            }

            args[pin.pinData.pinId] = pin.element.getElementsByClassName("data-input")[0].value;
        });

        return {
            nodeId: this.#data.nodeId,
            uniqueId: this.#uniqueId,
            x: this.#element.offsetLeft,
            y: this.#element.offsetTop,
            arguments: args
        };
    }

    toJsonConnections() {
        return this.#outPins.flatMap((pin) => {
            if (Object.keys(pin.connections).length === 0) {
                return [];
            }

            return Object.values(pin.connections).flatMap((connection) => {
                return {
                    fromNode: connection.parentPin.node.uniqueId,
                    fromPin: connection.parentPin.pinData.pinId,
                    toNode: connection.otherPin.node.uniqueId,
                    toPin: connection.otherPin.pinData.pinId,
                };
            });
        });
    }

    #setupEvents() {
        this.#element.addEventListener("contextmenu", (event) => {
            event.preventDefault();
            event.stopPropagation();
        });

        this.#element.getElementsByClassName("title")[0].addEventListener("mousedown", (event) => {
            event.preventDefault();
            event.stopPropagation();

            /** @param {MouseEvent} event */
            const onMouseMove = (event) => {
                event.preventDefault();
                event.stopPropagation();

                this.moveBy(event.movementX / this.#graph.scale, event.movementY / this.#graph.scale);
            };

            document.addEventListener("mousemove", onMouseMove);
            document.addEventListener("mouseup", () => {
                event.preventDefault();
                event.stopPropagation();

                document.removeEventListener("mousemove", onMouseMove);
            }, { once: true });
        });
    }
}