import { PinData } from "./PinData.js";

export class FlowPinData extends PinData
{
    constructor(jsonData, isInput) {
        super(jsonData, isInput);
    }
}