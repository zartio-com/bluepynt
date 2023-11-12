import { ArgumentPinData } from "./ArgumentPinData.js";
import { FlowPinData } from "./FlowPinData.js";

export class NodeData
{
    constructor(jsonData)
    {
        this.nodeId = jsonData.nodeId;
        this.baseType = jsonData.baseType;
        this.isPure = jsonData.isPure;
        this.name = jsonData.name;
        this.description = jsonData.description;
        this.inPins = this.#map_pins(jsonData.inPins, true);
        this.outPins = this.#map_pins(jsonData.outPins, false);
    }

    #map_pins(pins, isInput) {
        return pins.map((jsonData) => {
            switch (jsonData.pinType) {
                case "argument": {
                    return new ArgumentPinData(jsonData, isInput);
                }
                case "flow": {
                    return new FlowPinData(jsonData, isInput);
                }
            }
        });
    }
}