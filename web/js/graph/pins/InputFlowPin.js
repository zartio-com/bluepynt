import { PinBase } from "./PinBase.js";

export class InputFlowPin extends PinBase
{

    /** @type {OutputFlowPin | null} */
    #connectedPin = null;

    constructor(node, element, pinData) {
        super(node, element, pinData);
    }

    get isFlow() {
        return true;
    }
}