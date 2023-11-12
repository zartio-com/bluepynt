import { PinColors } from "./Types.js";

export class PinConnection
{

    /** @type {Pin} */
    #parentPin;

    /** @type {Pin} */
    #otherPin;

    /** @type {SVGLinearGradientElement|null} */
    #svgGradient = null;

    /** @type {SVGPathElement|null} */
    #svgPath = null;

    #inputColor = null;

    #outputColor = null;

    /**
     *
     * @param {Pin} parentPin
     * @param {Pin} otherPin
     */
    constructor(parentPin, otherPin) {
        this.#parentPin = parentPin;
        this.#otherPin = otherPin;

        this.#buildSvgPath();
        this.#setupEvents();
    }

    get parentPin() {
        return this.#parentPin;
    }

    get otherPin() {
        return this.#otherPin;
    }

    /** @returns {SVGPathElement|null} */
    get svgPath() {
        return this.#svgPath;
    }

    /** @returns {SVGLinearGradientElement|null} */
    get svgGradient() {
        return this.#svgGradient;
    }

    destroy() {
        if (this.#svgPath !== null) {
            this.#svgPath.remove();
        }

        if (this.#svgGradient !== null) {
            this.#svgGradient.remove();
        }

        this.#parentPin.node.removeEventListener("move", this.update);
        this.#otherPin.node.removeEventListener("move", this.update);
    }

    update() {
        const
            beginPoint = {
                x: this.parentPin.position.x + this.parentPin.element.offsetWidth,
                y: this.parentPin.position.y + this.parentPin.element.offsetHeight / 2 + 0.01
            },
            endPoint = {
                x: this.otherPin.position.x,
                y: this.otherPin.position.y + this.otherPin.element.offsetHeight / 2
            },
            curveOffset = Math.min(Math.max(Math.abs(beginPoint.x - endPoint.x), 70), 200),
            beginCurvePoint = {
                x: beginPoint.x + curveOffset,
                y: beginPoint.y
            },
            endCurvePoint = {
                x: endPoint.x - curveOffset,
                y: endPoint.y
            },
            box = this.#svgPath.getBBox(),
            cx = box.x + box.width / 2,
            cy = box.y + box.height / 2,
            radius = Math.sqrt(box.width * box.width + box.height * box.height) / 2,
            angle = (beginPoint.x > endPoint.x ? 180 : 0) * Math.PI / 180,
            rx = Math.cos(angle) * radius,
            ry = Math.sin(angle) * radius;


        if (beginPoint.x + 50 > endPoint.x) {
            this.#svgGradient.setAttribute("x1", "100%");
            this.#svgGradient.setAttribute("x2", "0%");
        } else {
            this.#svgGradient.setAttribute("x1", "0%");
            this.#svgGradient.setAttribute("x2", "100%");
        }
        //     this.#svgGradient.setAttribute("gradientTransform", `rotate(0)`);
        this.#svgPath.setAttribute(
            "d",
            `M${beginPoint.x} ${beginPoint.y} C${beginCurvePoint.x} ${beginCurvePoint.y} ${endCurvePoint.x} ${endCurvePoint.y} ${endPoint.x} ${endPoint.y}`
        );

        this.#outputColor.setAttribute("stop-color", PinColors[this.#parentPin.argumentType] ?? PinColors["undefined"]);
        this.#inputColor.setAttribute("stop-color", PinColors[this.#otherPin.argumentType] ?? PinColors["undefined"]);
    }

    #buildSvgPath() {
        const gradientId = `${this.#parentPin.node.uniqueId}-${this.#parentPin.pinData.pinId}_to_${this.#otherPin.node.uniqueId}-${this.#otherPin.pinData.pinId}`;
        this.#svgGradient = document.createElementNS("http://www.w3.org/2000/svg", "linearGradient");
        this.#svgGradient.setAttribute("id", gradientId);
        this.#svgGradient.setAttribute("x1", "0%");
        this.#svgGradient.setAttribute("y1", "0%");
        this.#svgGradient.setAttribute("x2", "100%");
        this.#svgGradient.setAttribute("y2", "0%");

        const stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
        stop1.setAttribute("offset", "49%");
        stop1.setAttribute("stop-color", PinColors[this.#parentPin.argumentType] ?? PinColors["undefined"]);
        this.#svgGradient.appendChild(stop1);
        this.#outputColor = stop1;

        const stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
        stop2.setAttribute("offset", "51%");
        stop2.setAttribute("stop-color", PinColors[this.#otherPin.argumentType] ?? PinColors["undefined"]);
        this.#svgGradient.appendChild(stop2);
        this.#inputColor = stop2;

        //this.#parentPin.node.graph.element.
        document.getElementById("connections").appendChild(this.#svgGradient);

        this.#svgPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
        //this.#svgPath.setAttribute("stroke", "url(#" + gradientId + ")");
        this.#svgPath.setAttribute("stroke", "url(#" + gradientId + ")");
        this.#svgPath.setAttribute("stroke-width", "3");
        this.#svgPath.setAttribute("fill", "none");
        document.getElementById("connections").appendChild(this.#svgPath);

        this.update();
    }

    #setupEvents() {
        this.#parentPin.node.addEventListener("move", this.update.bind(this));
        this.#otherPin.node.addEventListener("move", this.update.bind(this));
    }
}