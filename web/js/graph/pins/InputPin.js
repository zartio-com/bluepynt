import { PinBase } from "./PinBase.js";

export class InputPin extends PinBase
{

    /** @type {OutputPin | null} */
    connectedPin = null;

    constructor(node, element, pinData) {
        super(node, element, pinData);
    }

    connectTo(pin) {
        super.connectTo(pin);

        if (this.isConnected) {
            this.connectedPin.disconnect();
        }

        this.connectedPin = pin;
    }

    disconnect() {
        super.disconnect();

        if (this.isConnected === false) {
            return;
        }

        this.connectedPin.disconnect();
        this.connectedPin = null;
    }

    get isConnected() {
        return this.connectedPin !== null;
    }
}