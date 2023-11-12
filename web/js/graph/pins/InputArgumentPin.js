import { PinBase } from "./PinBase.js";

export class InputArgumentPin extends PinBase
{

    /** @type {OutputArgumentPin | null} */
    #connectedPin = null;

    constructor(node, element, pinData) {
        super(node, element, pinData);
    }

}