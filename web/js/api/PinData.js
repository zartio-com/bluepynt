
export class PinData
{
    constructor(jsonData, isInput) {
        this.pinId = jsonData.id;
        this.pinType = jsonData.pinType;
        this.name = jsonData.name;
        this.description = jsonData.description;
        this.isInput = isInput;
        this.isOutput = !isInput;
        this.typeDependsOn = jsonData.typeDependsOn;
    }
}