import { PinData } from "./PinData.js";

export class ArgumentPinData extends PinData
{
    constructor(jsonData, isInput) {
        super(jsonData, isInput);
        this.argumentType = jsonData.type;
        this.defaultValue = jsonData.defaultValue;
    }
}