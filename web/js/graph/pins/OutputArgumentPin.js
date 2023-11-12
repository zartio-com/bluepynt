import { PinBase } from "./PinBase.js";

export class OutputArgumentPin extends PinBase
{

    /** @type {Pin | null} */
    #connectedPin = null;

    constructor(node, element, pinData) {
        super(node, element, pinData);
    }

}