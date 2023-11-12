import os.path
from importlib.metadata import entry_points
from setuptools import setup
from setuptools.command.install import install
import subprocess

# If your plugin depends on other plugins, list them here
dependency_plugins: list[str] = []

# region Defaults - do not change


class InstallCommand(install):
    def run(self):
        if self.run_command('test') != 0:
            raise Exception(f"Tests failed, aborting installation. Contact plugin developer for more information.")
        install.run(self)


def run_tests():
    subprocess.call(['python', 'run_tests.py'])


for dependency in dependency_plugins:
    exists = any(ep.name == dependency for ep in entry_points(group="bluepynt.plugins"))
    if not exists:
        raise Exception(f"Missing dependency plugin: {dependency}")

install_requires = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt', 'r') as f:
        install_requires = f.read().splitlines()
# endregion

setup(
    name="Example Plugin",
    description="Example plugin to help you get started",
    version="1.0.0",
    author="Zartio.com",
    author_email="bluepynt@zartio.com",
    entry_points={
        "bluepynt.plugins": [
            "example_plugin = example_plugin.plugin:Plugin",
        ]
    },
    # Do not change, it will be auto-loaded from requirements.txt
    install_requires=install_requires,
    # Do not change, will run tests before installing to make sure plugin is compatible with current bluepynt version
    cmdclass={
        "install": InstallCommand,
    },
)
