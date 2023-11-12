from typing import Any

from pins import BaseFunctionNode, InputArgumentPin, OutputArgumentPin


class RerouteNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.RerouteNode", "Reroute", is_pure=True,
                         description="Reroutes the input to the output.",
                         in_pins=(
                             InputArgumentPin(pin_id="in", name="", argument_type=Any, type_depends_on="out"),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="out", name="", argument_type=Any, type_depends_on="in"),
                         ))

    def execute(self):
        self.output_pin("out").set_value(self.argument_pin("in").value)


# region Execution


class ReadVariableNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.ReadVariableNode", "Read Variable", is_pure=True,
                         description="Reads the value of the variable.",
                         in_pins=(
                             InputArgumentPin(pin_id="variable", name="Variable name", argument_type=str),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="value", name="Value", argument_type=Any),
                         ))

    def execute(self):
        variable = self.argument_pin("variable").value
        self.output_pin("value").set_value(self.parent_graph.variable(variable).value)


class WriteVariableNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.WriteVariableNode", "Write Variable",
                         description="Writes the value to the variable.",
                         in_pins=(
                             InputArgumentPin(pin_id="variable", name="Variable name", argument_type=str),
                             InputArgumentPin(pin_id="value", name="Value", argument_type=Any),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="value", name="Value", argument_type=Any),
                         ))

    def execute(self):
        variable = self.argument_pin("variable").value
        value = self.argument_pin("value").value
        self.parent_graph.variable(variable).set_value(value)
# endregion

# region Math


class AddNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.AddNode", "Add", is_pure=True,
                         description="Returns the sum of A and B.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=float | int),
                         ))

    def execute(self):
        self.output_pin("result").set_value(self.argument_pin("a").value + self.argument_pin("b").value)


class SubtractNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.SubtractNode", "Subtract", is_pure=True,
                         description="Returns the difference of A and B.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=float | int),
                         ))

    def execute(self):
        self.output_pin("result").set_value(self.argument_pin("a").value - self.argument_pin("b").value)


class MultiplyNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.MultiplyNode", "Multiply", is_pure=True,
                         description="Returns the product of A and B.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=float | int),
                         ))

    def execute(self):
        self.output_pin("result").set_value(self.argument_pin("a").value * self.argument_pin("b").value)


class DivideNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.DivideNode", "Divide", is_pure=True,
                         description="Returns the quotient of the division of A by B.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=float | int),
                         ))

    def execute(self):
        self.output_pin("result").set_value(self.argument_pin("a").value / self.argument_pin("b").value)


class ModuloNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.ModuloNode", "Modulo", is_pure=True,
                         description="Returns the remainder of the division of A by B.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=float | int),
                         ))

    def execute(self):
        self.output_pin("result").set_value(self.argument_pin("a").value % self.argument_pin("b").value)


class PowerNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.PowerNode", "Power", is_pure=True,
                         description="Returns the value of A raised to the power of B.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=float | int),
                         ))

    def execute(self):
        self.output_pin("result").set_value(self.argument_pin("a").value ** self.argument_pin("b").value)


class NegateNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.NegateNode", "Negate", is_pure=True,
                         description="Negates the value.",
                         in_pins=(
                             InputArgumentPin(pin_id="value", name="Value", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=float | int),
                         ))

    def execute(self):
        self.output_pin("result").set_value(-self.argument_pin("value").value)


class AbsNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.AbsNode", "Abs", is_pure=True,
                         description="Returns the absolute value of the given value.",
                         in_pins=(
                             InputArgumentPin(pin_id="value", name="Value", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=float | int),
                         ))

    def execute(self):
        self.output_pin("result").set_value(abs(self.argument_pin("value").value))


class FloorNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.FloorNode", "Floor", is_pure=True,
                         description="Rounds the value down to the nearest integer.",
                         in_pins=(
                             InputArgumentPin(pin_id="value", name="Value", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=int),
                         ))

    def execute(self):
        self.output_pin("result").set_value(int(self.argument_pin("value").value))


class CeilNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.CeilNode", "Ceil", is_pure=True,
                         description="Returns the smallest integer greater than or equal to the given value.",
                         in_pins=(
                             InputArgumentPin(pin_id="value", name="Value", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=int),
                         ))

    def execute(self):
        self.output_pin("result").set_value(int(self.argument_pin("value").value) + 1)


class RoundNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.RoundNode", "Round", is_pure=True,
                         description="Rounds the value to the given number of digits.",
                         in_pins=(
                             InputArgumentPin(pin_id="value", name="Value", argument_type=float | int),
                             InputArgumentPin(pin_id="n_digits", name="Digits", argument_type=int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=int),
                         ))

    def execute(self):
        self.output_pin("result").set_value(round(self.argument_pin("value").value,
                                                  self.argument_pin("n_digits").value))


class MinNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.MinNode", "Min", is_pure=True,
                         description="Returns the smallest of the given values.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=float | int),
                         ))

    def execute(self):
        a = self.argument_pin("a").value
        b = self.argument_pin("b").value
        self.output_pin("result").set_value(a if a < b else b)


class MaxNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.MaxNode", "Max", is_pure=True,
                         description="Returns the greater of two values.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=float | int),
                         ))

    def execute(self):
        a = self.argument_pin("a").value
        b = self.argument_pin("b").value
        self.output_pin("result").set_value(a if a > b else b)


class ClampNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.ClampNode", "Clamp", is_pure=True,
                         description="Clamps the value between min and max.",
                         in_pins=(
                             InputArgumentPin(pin_id="value", name="Value", argument_type=float | int),
                             InputArgumentPin(pin_id="min", name="Min", argument_type=float | int),
                             InputArgumentPin(pin_id="max", name="Max", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=float | int),
                         ))

    def execute(self):
        value = self.argument_pin("value").value
        v_min = self.argument_pin("min").value
        v_max = self.argument_pin("max").value
        self.output_pin("result").set_value(v_min if value < v_min else v_max if value > v_max else value)


class LerpNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.LerpNode", "Lerp", is_pure=True,
                         description="Linearly interpolates between A and B by T.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int),
                             InputArgumentPin(pin_id="t", name="T", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=float | int),
                         ))

    def execute(self):
        a = self.argument_pin("a").value
        b = self.argument_pin("b").value
        t = self.argument_pin("t").value
        self.output_pin("result").set_value(a + (b - a) * t)


class SignNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.SignNode", "Sign", is_pure=True,
                         description="Returns -1 if the value is less than zero, 1 if the value is greater than zero.",
                         in_pins=(
                             InputArgumentPin(pin_id="value", name="Value", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=int),
                         ))

    def execute(self):
        value = self.argument_pin("value").value
        self.output_pin("result").set_value(-1 if value < 0 else 1 if value > 0 else 0)


class IsPositiveNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.IsPositiveNode", "Is Positive", is_pure=True,
                         description="Returns true if the value is greater than zero.",
                         in_pins=(
                             InputArgumentPin(pin_id="value", name="Value", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        value = self.argument_pin("value").value
        self.output_pin("result").set_value(value > 0)


class IsNegativeNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.IsNegativeNode", "Is Negative", is_pure=True,
                         description="Returns true if the value is negative.",
                         in_pins=(
                             InputArgumentPin(pin_id="value", name="Value", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        value = self.argument_pin("value").value
        self.output_pin("result").set_value(value < 0)


class IsZeroNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.IsZeroNode", "Is Zero", is_pure=True,
                         description="Returns true if the value is equal to zero.",
                         in_pins=(
                             InputArgumentPin(pin_id="value", name="Value", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        value = self.argument_pin("value").value
        self.output_pin("result").set_value(value == 0)


class IsEqualNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.IsEqualNode", "Is Equal", is_pure=True,
                         description="Returns true if A is equal to B.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int | str),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int | str),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        a = self.argument_pin("a").value
        b = self.argument_pin("b").value
        self.output_pin("result").set_value(str(a) == str(b))
# endregion

# region Logic


class AndNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.AndNode", "And", is_pure=True,
                         description="Returns true if A and B are true.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=bool),
                             InputArgumentPin(pin_id="b", name="B", argument_type=bool),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        a = self.argument_pin("a").value
        b = self.argument_pin("b").value
        self.output_pin("result").set_value(a and b)


class OrNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.OrNode", "Or", is_pure=True,
                         description="Returns true if A or B are true.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=bool),
                             InputArgumentPin(pin_id="b", name="B", argument_type=bool),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        a = self.argument_pin("a").value
        b = self.argument_pin("b").value
        self.output_pin("result").set_value(a or b)


class NotNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.NotNode", "Not", is_pure=True,
                         description="Returns true if A is false.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=bool),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        a = self.argument_pin("a").value
        self.output_pin("result").set_value(not a)


class XorNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.XorNode", "Xor", is_pure=True,
                         description="Returns true if A or B are true, but not both.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=bool),
                             InputArgumentPin(pin_id="b", name="B", argument_type=bool),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        a = self.argument_pin("a").value
        b = self.argument_pin("b").value
        self.output_pin("result").set_value(a != b)


class IfNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.IfNode", "If", is_pure=True,
                         description="Returns A if Condition is true, otherwise returns B.",
                         in_pins=(
                             InputArgumentPin(pin_id="condition", name="Condition", argument_type=bool),
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int | str),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int | str),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result",
                                               argument_type=float | int | str),
                         ))

    def execute(self):
        condition = self.argument_pin("condition").value
        a = self.argument_pin("a").value
        b = self.argument_pin("b").value
        self.output_pin("result").set_value(a if condition else b)


class EqualNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.EqualNode", "Equal", is_pure=True,
                         description="Returns true if A is equal to B.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int | str),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int | str),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        a = self.argument_pin("a").value
        b = self.argument_pin("b").value
        self.output_pin("result").set_value(a == b)


class NotEqualNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.NotEqualNode", "Not Equal", is_pure=True,
                         description="Returns true if A is not equal to B.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int | str),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int | str),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        a = self.argument_pin("a").value
        b = self.argument_pin("b").value
        self.output_pin("result").set_value(a != b)


class GreaterNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.GreaterNode", "Greater", is_pure=True,
                         description="Returns true if A is greater than B.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        a = self.argument_pin("a").value
        b = self.argument_pin("b").value
        self.output_pin("result").set_value(a > b)


class GreaterEqualNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.GreaterEqualNode", "Greater Equal", is_pure=True,
                         description="Returns true if A is greater than or equal to B.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        a = self.argument_pin("a").value
        b = self.argument_pin("b").value
        self.output_pin("result").set_value(a >= b)


class LessNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.LessNode", "Less", is_pure=True,
                         description="Returns true if A is less than B.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        a = self.argument_pin("a").value
        b = self.argument_pin("b").value
        self.output_pin("result").set_value(a < b)


class LessEqualNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.LessEqualNode", "Less Equal", is_pure=True,
                         description="Returns true if A is less than or equal to B.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=float | int),
                             InputArgumentPin(pin_id="b", name="B", argument_type=float | int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        a = self.argument_pin("a").value
        b = self.argument_pin("b").value
        self.output_pin("result").set_value(a <= b)


class NandNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.NandNode", "Nand", is_pure=True,
                         description="Returns true if A and B are false.",
                         in_pins=(
                             InputArgumentPin(pin_id="a", name="A", argument_type=bool),
                             InputArgumentPin(pin_id="b", name="B", argument_type=bool),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=bool),
                         ))

    def execute(self):
        a = not self.argument_pin("a").value
        b = not self.argument_pin("b").value
        self.output_pin("result").set_value(a or b)
# endregion


# region Conversions


class IntToStringNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.IntToStringNode", "Int to String", is_pure=True,
                         description="Converts the integer value to a string.",
                         in_pins=(
                             InputArgumentPin(pin_id="value", name="Value", argument_type=int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=str),
                         ))

    def execute(self):
        self.output_pin("result").set_value(str(self.argument_pin("value").value))
# endregion

# region Constants


class ConstantIntNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.ConstantIntNode", "Constant Int", is_pure=True,
                         description="Returns the constant integer value.",
                         in_pins=(
                             InputArgumentPin(pin_id="value", name="Value", argument_type=int),
                         ),
                         out_pins=(
                             OutputArgumentPin(pin_id="result", name="Result", argument_type=int),
                         ))

    def execute(self):
        self.output_pin("result").set_value(self.argument_pin("value").value)
# endregion


NODE_MAP = {
    "bluepynt.builtin.RerouteNode": RerouteNode,
    "bluepynt.builtin.ReadVariableNode": ReadVariableNode,
    "bluepynt.builtin.WriteVariableNode": WriteVariableNode,
    "bluepynt.builtin.AddNode": AddNode,
    "bluepynt.builtin.SubtractNode": SubtractNode,
    "bluepynt.builtin.MultiplyNode": MultiplyNode,
    "bluepynt.builtin.DivideNode": DivideNode,
    "bluepynt.builtin.ModuloNode": ModuloNode,
    "bluepynt.builtin.PowerNode": PowerNode,
    "bluepynt.builtin.NegateNode": NegateNode,
    "bluepynt.builtin.AbsNode": AbsNode,
    "bluepynt.builtin.FloorNode": FloorNode,
    "bluepynt.builtin.CeilNode": CeilNode,
    "bluepynt.builtin.RoundNode": RoundNode,
    "bluepynt.builtin.MinNode": MinNode,
    "bluepynt.builtin.MaxNode": MaxNode,
    "bluepynt.builtin.ClampNode": ClampNode,
    "bluepynt.builtin.LerpNode": LerpNode,
    "bluepynt.builtin.SignNode": SignNode,
    "bluepynt.builtin.IsPositiveNode": IsPositiveNode,
    "bluepynt.builtin.IsNegativeNode": IsNegativeNode,
    "bluepynt.builtin.IsZeroNode": IsZeroNode,
    "bluepynt.builtin.IsEqualNode": IsEqualNode,
    "bluepynt.builtin.AndNode": AndNode,
    "bluepynt.builtin.OrNode": OrNode,
    "bluepynt.builtin.NotNode": NotNode,
    "bluepynt.builtin.XorNode": XorNode,
    "bluepynt.builtin.IfNode": IfNode,
    "bluepynt.builtin.EqualNode": EqualNode,
    "bluepynt.builtin.NotEqualNode": NotEqualNode,
    "bluepynt.builtin.GreaterNode": GreaterNode,
    "bluepynt.builtin.GreaterEqualNode": GreaterEqualNode,
    "bluepynt.builtin.LessNode": LessNode,
    "bluepynt.builtin.LessEqualNode": LessEqualNode,
    "bluepynt.builtin.NandNode": NandNode,
    "bluepynt.builtin.ConstantIntNode": ConstantIntNode,
    "bluepynt.builtin.IntToStringNode": IntToStringNode,
}
