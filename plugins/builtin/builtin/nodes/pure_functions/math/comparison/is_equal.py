from bluepynt import BaseFunctionNode, InputArgumentPin, OutputArgumentPin


class IsEqualNode(BaseFunctionNode):
    ID: str = "builtin.IsEqualNode"
    NAME: str = "Is Equal"
    DESCRIPTION: str = "Checks if two values are equal"
    CATEGORY: str = "Math|Comparison"

    def __init__(self):
        super().__init__(node_id=self.ID, name=self.NAME, description=self.DESCRIPTION, category=self.CATEGORY)
        self.in_pins = (
            InputArgumentPin(pin_id="a", name="A", argument_type=int | float),
            InputArgumentPin(pin_id="b", name="B", argument_type=int | float),
        )
        self.out_pins = (
            OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
        )

    def execute(self):
        self.output_pin("result").set_value(self.argument_pin("a").value == self.argument_pin("b").value)
