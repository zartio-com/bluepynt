import { Node } from "./Node.js";
import { PinData } from "../api/PinData.js";
import { ArgumentPinData } from "../api/ArgumentPinData.js";
import { FlowPinData } from "../api/FlowPinData.js";
import {ArePinsCompatible, PinColors} from "./Types.js";
import { PinConnection } from "./PinConnection.js";

export class Pin extends EventTarget
{
    /** @type {Node} */
    #node;

    /** @type {HTMLElement} */
    #element;

    /** @type {PinData|ArgumentPinData|FlowPinData} */
    #pinData;

    /** @type {boolean} */
    #isFlow;

    /** @type {boolean} */
    #isArgument;

    /** @type {Pin} */
    #connectedPin = null;

    /** @type {SVGPathElement|null} */
    #connectionPath = null;

    /** @type {boolean} */
    #isInput;

    /** @type {boolean} */
    #isOutput;

    /** @type {string} */
    argumentType;

    /** @type {PinConnection[]} */
    #connections = [];

    /**
     * Used for input pins.
     *
     * @type {Pin|null}
     */
    inputConnectedPin = null;

    /**
     *
     * @param {Node} node
     * @param {HTMLElement} element
     * @param {PinData|ArgumentPinData|FlowPinData} pinData
     * @param {boolean} isInput
     */
    constructor(node, element, pinData, isInput) {
        super();
        this.#node = node;
        this.#element = element;
        this.#pinData = pinData;
        this.#isFlow = pinData.pinType === "flow"
        this.#isArgument = !this.#isFlow;
        this.#isInput = isInput;
        this.#isOutput = !this.#isInput;
        this.argumentType = pinData.argumentType;

        this.#setupEvents();
    }

    get node() {
        return this.#node;
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
     * @returns {PinData|ArgumentPinData|FlowPinData}
     */
    get pinData() {
        return this.#pinData;
    }

    /**
     *
     * @returns {boolean}
     */
    get isFlow() {
        return this.#isFlow;
    }

    /**
     *
     * @returns {boolean}
     */
    get isArgument() {
        return this.#isArgument;
    }

    /**
     *
     * @returns {Pin|null}
     */
    get connectedPin() {
        return this.#connectedPin;
    }

    get position() {
        // return {
        //     x: this.#element.getBoundingClientRect().left,
        //     y: this.#element.getBoundingClientRect().top
        // }
        return {
            x: this.#node.position.x + this.#element.offsetLeft,
            y: this.#node.position.y + this.#element.offsetTop
        };
    }

    /**
     *
     * @returns {boolean}
     */
    get isConnected() {
        return this.inputConnectedPin !== null || Object.keys(this.#connections).length > 0;
    }

    /**
     *
     * @returns {boolean}
     */
    get isInput() {
        return this.#isInput;
    }

    /**
     *
     * @returns {boolean}
     */
    get isOutput() {
        return this.#isOutput;
    }

    /**
     *
     * @returns {PinConnection[]}
     */
    get connections() {
        return this.#connections;
    }

    /**
     *
     * @param {Pin} inputPin
     */
    connectTo(inputPin) {
        /** Connection happens on the output pin **/
        if (this.isInput) {
            if (inputPin.isOutput === false) {
                return;
            }

            inputPin.connectTo(this);
            return;
        }

        if (ArePinsCompatible(this, inputPin) === false) {
            return;
        }

        if (inputPin.isConnected) {
            inputPin.disconnect();
        }

        if (this.isConnected && this.isFlow) {
            Object.values(this.#connections).forEach((pinConnection) => {
                this.disconnect(pinConnection.otherPin);
            });
        }

        this.element.classList.add("connected");
        inputPin.element.classList.add("connected");
        inputPin.inputConnectedPin = this;

        if (this.argumentType === "Any") {
            this.changeDynamicType(inputPin.argumentType)
        }

        if (inputPin.argumentType === "Any") {
            inputPin.changeDynamicType(this.argumentType)
        }

        const
            connectionId = inputPin.node.uniqueId + "-" + inputPin.pinData.pinId;
        this.#connections[connectionId] = new PinConnection(this, inputPin);

        this.update();
    }

    /**
     *
     * @param {Pin|null} inputPin
     */
    disconnect(inputPin = null) {
        /** Disconnection happens on the output pin **/
        if (this.isInput) {
            if (inputPin === null && this.isConnected) {
                this.inputConnectedPin.disconnect(this);
                return;
            }

            if (inputPin.isInput) {
                return;
            }

            inputPin.disconnect(this);
        }

        if (inputPin === null) {
            return;
        }

        inputPin.element.classList.remove("connected");
        inputPin.inputConnectedPin = null;
        inputPin.update();

        const
            connectionId = inputPin.node.uniqueId + "-" + inputPin.pinData.pinId,
            connection = this.#connections[connectionId];
        if (connection === undefined) {
            return;
        }

        connection.destroy();
        delete this.#connections[connectionId];
        if (this.isConnected === false) {
            this.element.classList.remove("connected");

            if (this.node.findPinsDependingOn(this.pinData.pinId).some((pin) => pin.isConnected) === false) {
                this.changeDynamicType(this.pinData.argumentType);
            }
        }

        this.update();
    }

    update() {
        this.node.moveBy(0, 0);
        this.element.querySelector(".description-tooltip .type span").dataset.pinType = this.argumentType;
        this.element.getElementsByClassName("pin-indicator")[0].style.setProperty(
            "--pin-color",
            PinColors[this.argumentType] ?? PinColors["undefined"]
        );
    }

    changeDynamicType(newType) {
        this.argumentType = newType;
        this.update();

        const dependantPins = this.node.findPinsDependingOn(this.pinData.pinId);
        for (const pin of dependantPins) {
            pin.argumentType = newType;
            pin.update();

            if (pin.inputConnectedPin !== null) {
                pin.inputConnectedPin.changeDynamicType(newType);
            }

            if (Object.keys(pin.#connections).length > 0) {
                for (const connection of Object.values(pin.#connections)) {
                    connection.otherPin.changeDynamicType(newType);
                }
            }
        }
    }

    /**
     *
     * @param {Pin} pin
     * @returns {PinConnection|null}
     */
    findPinConnection(pin) {
        const found = this.#connections.find((pinConnection) => {
            return pinConnection.otherPin.pinData.pinId === pin.pinData.pinId
                && pinConnection.otherPin.node.uniqueId === pin.node.uniqueId;
        });

        return found ?? null;
    }

    /**
     *
     * @param {Node} node
     * @param {PinData} pinData
     * @param {boolean} isInput
     */
    static build(node, pinData, isInput) {
        if (isInput) {
            return new Pin(node, this.#buildInputPinElement(node, pinData), pinData, true);
        }

        return new Pin(node, this.#buildOutputPinElement(node, pinData), pinData, false);
    }

    /**
     *
     * @param {Node} node
     * @param {PinData|ArgumentPinData|FlowPinData} pinData
     * @returns {Node}
     */
    static #buildInputPinElement(node, pinData) {
        return this.#buildPinElement(node, "input-pin-template", pinData);
    }

    /**
     *
     * @param {Node} node
     * @param {PinData|ArgumentPinData|FlowPinData} pinData
     * @returns {Node}
     */
    static #buildOutputPinElement(node, pinData) {
        return this.#buildPinElement(node, "output-pin-template", pinData);
    }

    /**
     *
     * @param {Node} node
     * @param {string} templateElement
     * @param {PinData|ArgumentPinData|FlowPinData} pinData
     * @returns {Node}
     */
    static #buildPinElement(node, templateElement, pinData) {
        const pinElement = document.getElementById(templateElement).cloneNode(true);
        pinElement.id = "";

        if (pinData.pinType === "argument") {
            pinElement.classList.add("pin-input");
        } else {
            pinElement.classList.add("pin-exec");
            for (const element of pinElement.querySelectorAll(".data-input")) {
                element.remove();
            }
        }

        pinElement.getElementsByClassName("pin-title")[0].innerHTML = pinData.name;

        pinElement.dataset.nodeId = node.data.nodeId;
        pinElement.dataset.nodeUniqueId = node.uniqueId;

        pinElement.dataset.pinId = pinData.pinId;
        pinElement.dataset.pinType = pinData.pinType;
        pinElement.dataset.pinName = pinData.name;
        pinElement.dataset.pinDescription = pinData.description;

        pinElement.querySelector(".description-tooltip .type span").dataset.pinType = pinData.argumentType;

        pinElement.getElementsByClassName("pin-indicator")[0].style.setProperty("--pin-color", PinColors[pinData.argumentType] ?? PinColors["undefined"]);

        return pinElement;
    }

    #setupEvents() {
        // Pin connection
        this.#element.addEventListener("mousedown", (event) => {
            if (event.target.tagName === "INPUT") {
                return;
            }

            event.preventDefault();
            event.stopPropagation();

            const connectionsSVG = document.getElementById("connections");

            const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
            connectionsSVG.appendChild(path)

            let beginX, beginY, destinationX, destinationY;
            if (this.pinData.isOutput) {
                beginX = this.position.x + this.#element.offsetWidth;
                beginY = this.position.y + this.#element.offsetHeight / 2;
            } else {
                destinationX = this.position.x;
                destinationY = this.position.y + this.#element.offsetHeight / 2;
            }

            path.setAttribute("stroke", "white");
            path.setAttribute("stroke-width", "3");
            path.setAttribute("fill", "none");

            const onMouseMove = (event) => {
                event.preventDefault();
                event.stopPropagation();

                const graphRect = this.#node.graph.element.getBoundingClientRect();

                if (this.pinData.isOutput) {
                    const destination = {
                        x: Math.abs((graphRect.x - Math.max(event.pageX, graphRect.x)) / this.node.graph.scale),
                        y: Math.abs((graphRect.y - Math.max(event.pageY, graphRect.y)) / this.node.graph.scale)
                    };
                    destinationX = destination.x;
                    destinationY = destination.y;
                } else {
                    const begin = {
                        x: Math.abs((graphRect.x - Math.max(event.pageX, graphRect.x)) / this.node.graph.scale),
                        y: Math.abs((graphRect.y - Math.max(event.pageY, graphRect.y)) / this.node.graph.scale)
                    };
                    beginX = begin.x;
                    beginY = begin.y;
                }

                const
                    curveOffset = Math.min(Math.max(Math.abs(beginX - destinationX), 70), 200),
                    beginCurveX = beginX + curveOffset,
                    destinationCurveX = destinationX - curveOffset;

                path.setAttribute(
                    "d",
                    `M${beginX} ${beginY} C${beginCurveX} ${beginY} ${destinationCurveX} ${destinationY} ${destinationX} ${destinationY}`
                );
            }

            document.addEventListener("mousemove", onMouseMove);

            document.addEventListener("mouseup", (event) => {
                event.preventDefault();
                event.stopPropagation();

                document.removeEventListener("mousemove", onMouseMove);

                path.remove();

                const element = document.elementFromPoint(event.clientX, event.clientY);
                if (element === null) {
                    return;
                }

                const pinElement = element.closest(".pin");
                if (pinElement === null) {
                    return;
                }

                const pin = this.#node.graph.findPinByHTMLElement(pinElement);
                if (pin === null) {
                    return;
                }

                this.connectTo(pin);
            }, { once: true });
        });
    }
}