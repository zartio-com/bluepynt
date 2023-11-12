from bluepynt import PluginBase


class StableDiffusion(PluginBase):
    def __init__(self):
        super().__init__(
            name="Stable Diffusion",
            description="Base SD plugin to enable inference"
        )

    def initialize(self):
        pass

    def load_nodes(self):
        return []
