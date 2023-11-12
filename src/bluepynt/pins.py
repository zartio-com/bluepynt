from abc import abstractmethod
from types import UnionType
from typing import Callable, Any


def sanitize_value(value, value_type: type | UnionType):
    if isinstance(value, str) and not isinstance(value, value_type):
        if value_type is int:
            value = int(value)
        if value_type is float:
            value = float(value)
        if value_type is int | float:
            if "." in value:
                value = float(value)
            else:
                value = int(value)

    if value_type is Any:
        return value

    if not isinstance(value, value_type):
        raise ValueError(f"Value {value} is not of type {value_type} and could not be converted to it")

    return value


class Graph:
    def __init__(self,
                 main_node: 'Node', nodes: tuple['Node'] = (),
                 variables: tuple['GraphVariable'] = ()):
        self.main_node = main_node
        self.nodes = nodes
        self.variables = variables

        for node in self.nodes:
            node.parent_graph = self

    def execute(self):
        self.main_node.execute()

    def node(self, unique_id: str) -> 'Node':
        for node in self.nodes:
            if node.unique_id == unique_id:
                return node

        raise Exception(f"Node {unique_id} not found in graph")

    def variable(self, variable_name: str) -> 'GraphVariable':
        for variable in self.variables:
            if variable.name == variable_name:
                return variable

        raise Exception(f"Variable {variable_name} not found in graph")


class GraphVariable:
    def __init__(self, name: str, variable_type: type | UnionType, default_value=None):
        self.name = name
        self.type = variable_type
        self.default_value = default_value
        self._value = self.default_value

    @property
    def value(self):
        return self._value

    def set_value(self, value):
        self._value = sanitize_value(value, self.type)


class Node:
    ID: str = "undefined"

    def __init__(self, node_id: str, name: str,
                 in_pins: tuple['Pin'] | tuple = (), out_pins: tuple['Pin'] | tuple = (),
                 is_pure: bool = False, description: str = "", category: str = ""):
        self.node_id = node_id
        self.name = name
        self.is_pure = is_pure
        self.in_pins = in_pins
        self.out_pins = out_pins
        self.description = description
        self.category = category

        # Runtime properties
        self.unique_id = None
        self.parent_graph: Graph | None = None

        for pin in self.in_pins:
            pin.parent_node = self

        for pin in self.out_pins:
            pin.parent_node = self

    def output_flow_pin(self, pin_id: str) -> 'OutputFlowPin':
        for pin in self.out_pins:
            if pin.pin_id == pin_id and isinstance(pin, OutputFlowPin):
                return pin

        raise Exception(f"Pin {pin_id} not found in node {self.node_id}")

    def input_flow_pin(self, pin_id: str) -> 'InputFlowPin':
        for pin in self.in_pins:
            if pin.pin_id == pin_id and isinstance(pin, InputFlowPin):
                return pin

        raise Exception(f"Pin {pin_id} not found in node {self.node_id}")

    def argument_pin(self, pin_id: str) -> 'InputArgumentPin':
        for pin in self.in_pins:
            if pin.pin_id == pin_id and isinstance(pin, InputArgumentPin):
                return pin

        raise Exception(f"Pin {pin_id} not found in node {self.node_id}")

    def output_pin(self, pin_id: str) -> 'OutputArgumentPin':
        for pin in self.out_pins:
            if pin.pin_id == pin_id and isinstance(pin, OutputArgumentPin):
                return pin

        raise Exception(f"Pin {pin_id} not found in node {self.node_id}")

    def any_output_pin(self, pin_id: str) -> 'Pin':
        for pin in self.out_pins:
            if pin.pin_id == pin_id:
                return pin

        raise Exception(f"Pin {pin_id} not found in node {self.node_id}")

    def any_input_pin(self, pin_id: str) -> 'Pin':
        for pin in self.in_pins:
            if pin.pin_id == pin_id:
                return pin

        raise Exception(f"Pin {pin_id} not found in node {self.node_id}")

    def execute(self):
        pass

    def to_json(self):
        return {
            "id": self.node_id,
            "nodeId": self.node_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "inPins": [pin.to_json() for pin in self.in_pins],
            "outPins": [pin.to_json() for pin in self.out_pins]
        }


class BaseFunctionNode(Node):
    def __init__(self, node_id: str, name: str,
                 in_pins: tuple['Pin'] | tuple = (), out_pins: tuple['Pin'] | tuple = (),
                 is_pure: bool = False, description: str = "", category: str = ""):
        if any(isinstance(i, FlowPin) for i in in_pins):
            raise Exception("Input pins cannot be flow pins for functions nodes. If you want to use flow pins, "
                            "extend BaseMacroNode instead.")
        if any(isinstance(i, FlowPin) for i in out_pins):
            raise Exception("Output pins cannot be flow pins for functions nodes. If you want to use flow pins, "
                            "extend BaseMacroNode instead.")

        if not is_pure:
            in_pins = (InputFlowPin(pin_id="exec_in", name="", execute_method=self.execute),) + in_pins
            out_pins = (OutputFlowPin(pin_id="exec_out", name=""),) + out_pins

        super().__init__(node_id, name, in_pins, out_pins, is_pure, description, category)

    def internal_execute(self):
        self.execute()
        self.output_flow_pin("exec_out").execute()

    @abstractmethod
    def execute(self):
        pass

    def to_json(self):
        return {
            "id": self.node_id,
            "nodeId": self.node_id,
            "baseType": "functions",
            "isPure": self.is_pure,
            "name": self.name,
            "description": self.description,
            "inPins": [pin.to_json() for pin in self.in_pins],
            "outPins": [pin.to_json() for pin in self.out_pins]
        }


class BaseMacroNode(Node):
    def __init__(self, node_id: str, name: str = "Default node name",
                 in_pins: tuple['Pin'] | tuple = (), out_pins: tuple['Pin'] | tuple = (), description: str = "",
                 category: str = ""):
        super().__init__(node_id, name, in_pins, out_pins, False, description, category)

    def to_json(self):
        return {
            "id": self.node_id,
            "nodeId": self.node_id,
            "baseType": "macro",
            "name": self.name,
            "description": self.description,
            "inPins": [pin.to_json() for pin in self.in_pins],
            "outPins": [pin.to_json() for pin in self.out_pins]
        }


class Pin:
    def __init__(self, pin_id: str, name: str, description: str = ""):
        self.parent_node: Node | None = None
        self.pin_id = pin_id
        self.name = name
        self.description = description

    def to_json(self):
        return {
            "id": self.pin_id,
            "name": self.name,
            "description": self.description
        }


class ArgumentPin(Pin):
    def __init__(self, pin_id: str, name: str, argument_type: type | UnionType, description: str = "",
                 type_depends_on: str = None):
        super().__init__(pin_id, name, description)
        self.type = argument_type
        self.type_depends_on = type_depends_on

        # Runtime properties
        self._value = None

    @property
    def value(self):
        return self._value

    def set_value(self, value):
        self._value = sanitize_value(value, self.type)


class OutputArgumentPin(ArgumentPin):
    def __init__(self, pin_id: str, name: str, argument_type: type | UnionType, description: str = "",
                 type_depends_on: str = None):
        super().__init__(pin_id, name, argument_type, description, type_depends_on)
        self._value = None

    @property
    def value(self):
        # self._value is None and
        if isinstance(self.parent_node, BaseFunctionNode) and self.parent_node.is_pure:
            self.parent_node.execute()
        return self._value

    def connect(self, destination_pin: 'InputArgumentPin'):
        destination_pin.connect(self)

    def to_json(self):
        return {
            "id": self.pin_id,
            "pinType": "argument",
            "name": self.name,
            "description": self.description,
            "type": str(self.type) if isinstance(self.type, UnionType) else self.type.__name__,
            "defaultValue": None,
            "typeDependsOn": self.type_depends_on
        }


class InputArgumentPin(ArgumentPin):
    def __init__(self, pin_id: str, name: str, argument_type: type | UnionType,
                 description: str = "", default_value=None, type_depends_on: str = None):
        super().__init__(pin_id, name, argument_type, description, type_depends_on)
        self._value = default_value

        # Runtime properties
        self.source_pin: OutputArgumentPin | None = None

    @property
    def value(self):
        if self.source_pin is not None:
            return self.source_pin.value
        return self._value

    def connect(self, source_pin: OutputArgumentPin):
        self.source_pin = source_pin

    def to_json(self):
        return {
            "id": self.pin_id,
            "pinType": "argument",
            "name": self.name,
            "description": self.description,
            "type": str(self.type) if isinstance(self.type, UnionType) else self.type.__name__,
            "defaultValue": str(self._value),
            "typeDependsOn": self.type_depends_on
        }


class FlowPin(Pin):
    def __init__(self, pin_id, name, description: str = ""):
        super().__init__(pin_id, name, description)

    def to_json(self):
        return {
            "id": self.pin_id,
            "pinType": "flow",
            "name": self.name,
            "description": self.description
        }


class InputFlowPin(FlowPin):
    def __init__(self, pin_id: str, name: str, execute_method: Callable, description: str = ""):
        super().__init__(pin_id, name, description)
        self.execute_method = execute_method

    def connect(self, source_pin: 'OutputFlowPin'):
        source_pin.connect(self)


class OutputFlowPin(FlowPin):
    def __init__(self, pin_id: str, name: str = "", description: str = ""):
        super().__init__(pin_id, name, description)

        # Runtime properties
        self.destination_pin: InputFlowPin | None = None

    def connect(self, destination_pin: InputFlowPin):
        self.destination_pin = destination_pin

    def execute(self):
        if self.destination_pin is None:
            return
        self.destination_pin.execute_method()
