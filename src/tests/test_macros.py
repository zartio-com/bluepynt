import unittest
from unittest.mock import patch

from builtin.macros import BranchNode, ForLoopNode


class TestMacros(unittest.TestCase):

    def test_branch(self):
        branch_node = BranchNode()
        branch_node.argument_pin("condition").set_value(True)

        with patch.object(branch_node.output_flow_pin("exec_true"), "execute") as mock:
            branch_node.execute()
            mock.assert_called_once()

        branch_node.argument_pin("condition").set_value(False)

        with patch.object(branch_node.output_flow_pin("exec_false"), "execute") as mock:
            branch_node.execute()
            mock.assert_called_once()

    def test_for_loop(self):
        for_loop_node = ForLoopNode()
        for_loop_node.argument_pin("start").set_value(0)
        for_loop_node.argument_pin("end").set_value(10)
        for_loop_node.argument_pin("step").set_value(1)

        with patch.object(for_loop_node.output_flow_pin("exec_body"), "execute") as mock:
            for_loop_node.execute()
            self.assertEqual(mock.call_count, 10)
