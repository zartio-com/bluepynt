import {ArePinsCompatible} from "../Types";

export class PinBase
{

    /** @type {Node} */
    node;

    /** @type {HTMLElement} */
    element;

    /** @type {PinData|FlowPinData|ArgumentPinData} */
    pinData;

    /**
     *
     * @param {Node} node
     * @param {HTMLElement} element
     * @param {PinData|FlowPinData|ArgumentPinData} pinData
     */
    constructor(node, element, pinData) {
        this.node = node;
        this.element = element;
        this.pinData = pinData;

        this._setupEvents();
    }

    /**
     *
     * @param {PinBase} pin
     * @returns boolean
     */
    connectTo(pin) {
        if (ArePinsCompatible(this, pin) === false) {
            return false;
        }
    }

    disconnect() {

    }

    _setupEvents() {

    }
}