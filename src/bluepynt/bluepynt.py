import json
import builtins

from bluepynt import mapping
from pins import Node, Graph, InputFlowPin, OutputFlowPin, InputArgumentPin, OutputArgumentPin, \
    GraphVariable

PIN_TYPE_MAP = {
    "input_flow_pin": InputFlowPin,
    "output_flow_pin": OutputFlowPin,
    "input_argument_pin": InputArgumentPin,
    "output_argument_pin": OutputArgumentPin,
}


def get_type(type_name):
    try:
        return getattr(builtins, type_name)
    except AttributeError:
        return None


class Bluepynt:
    @staticmethod
    def load_graph_from_structure(data) -> list[Graph]:
        graphs: list[Graph] = []

        for data_graph in data["graphs"]:
            nodes: list[Node] = []
            main_node: Node | None = None
            for data_node in data_graph["nodes"]:
                if data_node["nodeId"] not in mapping.NODE_MAP:
                    raise Exception(f"Node type {data_node['nodeId']} not found")

                node_id: type = mapping.NODE_MAP[data_node["nodeId"]]
                node = node_id()
                node.unique_id = data_node["uniqueId"]

                if isinstance(node, mapping.NODE_MAP["bluepynt.builtin.BeginNode"]):
                    main_node = node

                if "arguments" in data_node:
                    for pinId, value in data_node["arguments"].items():
                        node.argument_pin(pinId).set_value(value)

                nodes.append(node)

            if main_node is None:
                raise Exception("Main node not found")

            variables: list[GraphVariable] = []
            if "variables" in data_graph:
                for data_variable in data_graph["variables"]:
                    variable_type = get_type(data_variable["type"])
                    if variable_type is None:
                        raise Exception(f"Type {data_variable['type']} not found")

                    variable = GraphVariable(data_variable["name"], variable_type, data_variable["value"])
                    variables.append(variable)

            graph = Graph(main_node, tuple(nodes), tuple(variables))
            for connection in data_graph["connections"]:
                from_node = graph.node(connection["fromNode"])
                to_node = graph.node(connection["toNode"])
                from_pin = from_node.any_output_pin(connection["fromPin"])
                to_pin = to_node.any_input_pin(connection["toPin"])
                from_pin.connect(to_pin)

            graphs.append(graph)

        return graphs

    @staticmethod
    def load_graph_from_json(json_data) -> list[Graph]:
        data = json.loads(json_data)
        return Bluepynt.load_graph_from_structure(data)
