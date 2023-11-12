import importlib.util
import os.path
from importlib.metadata import entry_points

from setuptools import setup

dependency_plugins = ["Builtin"]
for dependency in dependency_plugins:
    exists = any(ep.name == dependency for ep in entry_points(group="bluepynt.plugins"))
    if not exists:
        raise Exception(f"Missing dependency plugin: {dependency}")

install_requires = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt', 'r') as f:
        install_requires = f.read().splitlines()

setup(
    name="Stable Diffusion",
    description="Base SD plugin to enable inference",
    version="1.0.0",
    install_requires=install_requires,
    entry_points={
        "bluepynt.plugins": [
            "Stable Diffusion = stable_diffusion.stable_diffusion:StableDiffusion",
        ]
    },
)
