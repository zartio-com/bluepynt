import unittest
from unittest.mock import patch, MagicMock

from bluepynt import Bluepynt


class TestBluepy(unittest.TestCase):
    @patch("bluepynt.builtin.nodes.ConsoleLogNode.execute")
    def test_build_graph_from_json(self, mock_console_log_node: MagicMock):
        json_data = """
        {
            "graphs": [
                {
                    "nodes": [
                        {
                            "nodeId": "bluepynt.builtin.BeginNode",
                            "uniqueId": "0"
                        },
                        {
                            "nodeId": "bluepynt.builtin.ConsoleLogNode",
                            "uniqueId": "1",
                            "arguments": {
                                "message": "Hello World!"
                            }
                        }
                    ],
                    "connections": [
                        {
                            "fromNode": "0",
                            "fromPin": "exec_out",
                            "toNode": "1",
                            "toPin": "exec_in"
                        }
                    ]
                }
            ]
        }
        """

        graphs = Bluepynt.load_graph_from_json(json_data)
        self.assertEqual(1, len(graphs))
        graph = graphs[0]
        self.assertEqual(2, len(graph.nodes))
        self.assertEqual(graph.node("0").output_flow_pin("exec_out").destination_pin,
                         graph.node("1").input_flow_pin("exec_in"))
        self.assertEqual("Hello World!", graph.node("1").argument_pin("message").value)

        graph.execute()
        mock_console_log_node.assert_called_once()
