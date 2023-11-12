from importlib.metadata import entry_points

from src.bluepynt import PluginBase, Node

print("Loading plugins...")
plugins: list[PluginBase] = []
plugin_eps = entry_points(group="bluepynt.plugins")
for plugin_ep in plugin_eps:
    plugins.append(plugin_ep.load()())
    print(f"Loaded plugin - {plugin_ep.name}")

NODE_MAP: dict[str, Node] = {}

print("Loading nodes...")
for plugin in plugins:
    new_nodes = plugin.load_nodes()
    NODE_MAP.update(map(lambda node: (node.ID, node), new_nodes))
    print(f"Loaded {len(new_nodes)} nodes from {plugin.name}")

print(NODE_MAP)
