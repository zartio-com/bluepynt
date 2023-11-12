from pins import Node, OutputFlowPin, BaseFunctionNode, InputArgumentPin


class BeginNode(Node):
    def __init__(self):
        super().__init__("bluepynt.builtin.BeginNode", "Begin",
                         description="This node is executed when the graph is loaded by the server.",
                         out_pins=(
                             OutputFlowPin(pin_id="exec_out"),
                         ))

    def execute(self):
        self.output_flow_pin("exec_out").execute()

# region Logging


class ConsoleLogNode(BaseFunctionNode):
    def __init__(self):
        super().__init__("bluepynt.builtin.ConsoleLogNode", "Console Log",
                         description="Logs a message to the console.",
                         in_pins=(
                             InputArgumentPin(pin_id="message", name="Message", argument_type=str),
                         ))

    def execute(self):
        print(self.argument_pin("message").value)
# endregion

# region StableDiffusion


# endregion


NODE_MAP = {
    "bluepynt.builtin.BeginNode": BeginNode,
    "bluepynt.builtin.ConsoleLogNode": ConsoleLogNode,
}
