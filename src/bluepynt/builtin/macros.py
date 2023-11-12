from typing import Any

from pins import OutputFlowPin, InputArgumentPin, BaseMacroNode, InputFlowPin, OutputArgumentPin


class ExecRerouteNode(BaseMacroNode):
    def __init__(self):
        super().__init__(node_id="bluepynt.builtin.ExecRerouteNode", name="Exec Reroute",
                         description="Reroutes the execution flow to another node")
        self.in_pins = (
            InputFlowPin(pin_id="exec_in", name="", execute_method=self.execute),
        )
        self.out_pins = (
            OutputFlowPin(pin_id="exec_out", name=""),
        )

    def execute(self):
        self.output_flow_pin("exec_out").execute()


class BranchNode(BaseMacroNode):
    def __init__(self):
        super().__init__(node_id="bluepynt.builtin.BranchNode", name="Branch",
                         description="Executes one of two branches based on a condition")
        self.in_pins = (
            InputFlowPin(pin_id="exec_in", name="", execute_method=self.execute),
            InputArgumentPin(pin_id="condition", name="Condition", argument_type=bool),
        )
        self.out_pins = (
            OutputFlowPin(pin_id="exec_true", name="True"),
            OutputFlowPin(pin_id="exec_false", name="False"),
        )

    def execute(self):
        if self.argument_pin("condition").value:
            return self.output_flow_pin("exec_true").execute()
        return self.output_flow_pin("exec_false").execute()


class ForLoopNode(BaseMacroNode):
    def __init__(self):
        super().__init__(node_id="bluepynt.builtin.ForLoopNode", name="For Loop",
                         description="Iterates over a range of numbers")
        self.in_pins = (
            InputFlowPin(pin_id="exec_in", name="", execute_method=self.execute),
            InputArgumentPin(pin_id="start", name="Start", argument_type=int),
            InputArgumentPin(pin_id="end", name="End", argument_type=int),
            InputArgumentPin(pin_id="step", name="Step", argument_type=int),
            InputFlowPin(pin_id="exec_break", name="Break", execute_method=self.execute),
        )
        self.out_pins = (
            OutputFlowPin(pin_id="exec_body", name="Loop body"),
            OutputArgumentPin(pin_id="i", name="Index", argument_type=int),
            OutputFlowPin(pin_id="exec_out", name="Completed"),
        )

        # Runtime properties
        self.should_break = False

    def execute(self):
        self.should_break = False
        start = self.argument_pin("start").value
        end = self.argument_pin("end").value
        step = self.argument_pin("step").value

        if step == 0:
            raise ValueError("Step cannot be zero")

        if step > 0:
            if start >= end:
                raise ValueError("Start must be less than end")
        else:
            if start <= end:
                raise ValueError("Start must be greater than end")

        for i in range(start, end + 1, step * 1 if start < end else -1):
            self.output_pin("i").set_value(i)
            self.output_flow_pin("exec_body").execute()

            if self.should_break:
                break

        self.output_flow_pin("exec_out").execute()

    def execute_break(self):
        self.should_break = True


class ForEachLoopNode(BaseMacroNode):
    def __init__(self):
        super().__init__(node_id="bluepynt.builtin.ForEachLoopNode", name="For Each Loop",
                         description="Iterates over a list")
        self.in_pins = (
            InputFlowPin(pin_id="exec_in", name="", execute_method=self.execute),
            InputArgumentPin(pin_id="list", name="List", argument_type=list[Any]),
            InputFlowPin(pin_id="exec_break", name="", execute_method=self.execute),
        )
        self.out_pins = (
            OutputFlowPin(pin_id="exec_body"),
            OutputArgumentPin(pin_id="item", name="Item", argument_type=Any),
            OutputFlowPin(pin_id="exec_out"),
        )

        # Runtime properties
        self.should_break = False

    def execute(self):
        self.should_break = False
        for item in self.argument_pin("list").value:
            self.output_pin("item").set_value(item)
            self.output_flow_pin("exec_body").execute()

            if self.should_break:
                break

        self.output_flow_pin("exec_out").execute()

    def execute_break(self):
        self.should_break = True


NODE_MAP = {
    "bluepynt.builtin.ExecRerouteNode": ExecRerouteNode,
    "bluepynt.builtin.BranchNode": BranchNode,
    "bluepynt.builtin.ForLoopNode": ForLoopNode,
    "bluepynt.builtin.ForEachLoopNode": ForEachLoopNode,
}
