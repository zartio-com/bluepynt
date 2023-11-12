/**
 *
 * @type {{str: string[], float: string[], int: string[]}}
 */
let Types = {
    "str": [
        "int", "float", "Any"
    ],
    "int": [
        "str", "float", "bool", "Any"
    ],
    "float": [
        "str", "int", "Any"
    ],
    "bool": [
        "int", "float", "Any"
    ],
    "Any": [
        "str", "int", "float", "bool", "Any"
    ]
};

let PinColors = {
    "undefined": "#fff",
    "str": "#ff6a00",
    "int": "#166b53",
    "float": "#166b53",
    "int | float": "#166b53",
    "float | int | str": "#166b53",
    "bool": "#700302",
}

/**
 *
 * @param {Pin|PinBase} pin1
 * @param {Pin|PinBase} pin2
 * @returns {boolean}
 */
const ArePinsCompatible = (pin1, pin2) => {
    if (pin1.node.uniqueId === pin2.node.uniqueId && pin1.pinData.pinId === pin2.pinData.pinId) {
        return false;
    }

    if (pin1.isInput && pin2.isInput) {
        return false;
    }

    if (pin1.isFlow && pin2.isFlow) {
        return true;
    }

    if (pin1.pinData.pinType !== pin2.pinData.pinType) {
        return false;
    }

    const
        type1 = pin1.argumentType?.replace(" ", ""),
        type2 = pin2.argumentType?.replace(" ", "");

    if (type1 === type2) {
        return true;
    }

    const pin1Options = type1.split("|");
    const pin2Options = type2.split("|");

    for (const pin1Type of pin1Options) {
        for (const pin2Type of pin2Options) {
            if (Types[pin1Type].includes(pin2Type)) {
                return true;
            }
        }
    }

    if (Types[type1].includes(type2)) {
        return true;
    }

    return false;
}

export {PinColors,ArePinsCompatible};