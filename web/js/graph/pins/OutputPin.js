import { PinBase } from "./PinBase.js";

export class OutputPin extends PinBase
{

    constructor(node, element, pinData) {
        super(node, element, pinData);
    }

    disconnect() {

    }

    _setupEvents() {
        super._setupEvents();
    }
}