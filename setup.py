# -*- coding: utf-8 -*-
from setuptools import setup, find_packages, Command
#
class test(Command):
    """Runs all "PYTHON" tests under the greww/folder
    """

    description = "run all tests"
    user_options = []  # distutils complains if this is not here.

    def __init__(self, *args):
        self.args = args[0]  # so we can pass it to other classes
        Command.__init__(self, *args)

    def initialize_options(self):  # distutils wants this
        pass

    def finalize_options(self):    # this too
        pass

    def run(self):
        import os

with open('README.md') as f:
    readme = f.read()
"""
with open('LICENSE') as f:
    license = f.read()
"""

setup(
    name='FaGit',
    version='0.0.1',
    description='fagit',
    long_description=readme,
    author='hilaly mohammed-amine',
    author_email='hilalyamine@gmail.com',
    cmdclass={'test' : test},
    py_modules=['fagit'],
    scripts=['bin/fagit'],
)
