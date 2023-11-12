from bluepynt import PluginBase
from builtin.nodes.pure_functions.math.comparison import IsEqualNode


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()

    def initialize(self):
        pass

    def load_nodes(self):
        return [
            IsEqualNode,
        ]
