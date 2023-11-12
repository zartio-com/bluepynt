import { PinBase } from "./PinBase.js";

export class OutputFlowPin extends PinBase
{

    /** @type {InputFlowPin | null} */
    connectedPin = null;

    constructor(node, element, pinData) {
        super(node, element, pinData);
    }

    /**
     *
     * @param {PinBase} pin
     * @returns {boolean}
     */
    connectTo(pin) {
        const base = super.connectTo(pin);
        if (base === false) {
            return false;
        }

        this.connectedPin = pin;
    }

    disconnect() {
        super.disconnect();
    }
}