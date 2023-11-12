import unittest

from builtin.nodes.pure_functions.math.comparison import IsEqualNode


class TestIsEqual(unittest.TestCase):
    def test_is_equal_int(self):
        node = IsEqualNode()
        node.argument_pin("a").set_value(1)
        node.argument_pin("b").set_value(1)
        node.execute()
        self.assertEqual(node.output_pin("result").value, True)

        node.argument_pin("a").set_value(1)
        node.argument_pin("b").set_value(2)
        node.execute()
        self.assertEqual(node.output_pin("result").value, False)

    def test_is_equal_float(self):
        node = IsEqualNode()
        node.argument_pin("a").set_value(1.0)
        node.argument_pin("b").set_value(1.0)
        node.execute()
        self.assertEqual(node.output_pin("result").value, True)

        node.argument_pin("a").set_value(1.0)
        node.argument_pin("b").set_value(1.01)
        node.execute()
        self.assertEqual(node.output_pin("result").value, False)

    def test_is_equal_mixed(self):
        node = IsEqualNode()
        node.argument_pin("a").set_value(1)
        node.argument_pin("b").set_value(1.0)
        node.execute()
        self.assertEqual(node.output_pin("result").value, True)

        node.argument_pin("a").set_value(1)
        node.argument_pin("b").set_value(2.0)
        node.execute()
        self.assertEqual(node.output_pin("result").value, False)


if __name__ == '__main__':
    unittest.main()
