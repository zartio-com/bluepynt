import os
import subprocess
import unittest

from multiprocessing import Process
from setuptools import setup, Command
from setuptools.command.install import install


class InstallCommand(install):
    def run(self):
        try:
            self.run_command('test')
        except:
            print(f"Tests failed, aborting installation. Contact plugin developer for more information.")
            return
        install.run(self)


setup(
    name="Bluepynt builtin nodes",
    description="Builtin nodes for Bluepynt",
    version="1.0.0",
    author="Zartio",
    author_email="bluepynt@zartio.com",

    entry_points={
        "bluepynt.plugins": [
            "bluepynt_builtin = builtin.plugin:Plugin",
        ]
    },
    test_suite="tests",
    cmdclass={
        "install": InstallCommand,
    },
)
