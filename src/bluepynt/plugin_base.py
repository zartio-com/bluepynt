from abc import abstractmethod

from bluepynt import Node


class PluginBase:
    def __init__(self):
        self.initialize()

    @abstractmethod
    def initialize(self) -> None:
        """
        This method is called when the plugin is loaded. If you need to do any initialization, do it here.
        """
        pass

    @abstractmethod
    def load_nodes(self) -> list[Node]:
        """
        Override this method and return a list of nodes that you want to be available in the editor.
        """
        return []
