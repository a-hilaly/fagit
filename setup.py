# -*- coding: utf-8 -*-
from setuptools import setup, find_packages, Command
#
class test(Command):

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
    name='fagit',
    version='0.0.2',
    description='fagit',
    long_description=readme,
    author='hilaly mohammed-amine',
    author_email='hilalyamine@gmail.com',
    cmdclass={'test' : test},
    packages=find_packages(exclude=('tests', 'docs', '.circleci')),
    scripts=['bin/fagit'],
    package_data={'fagit': ['conf/conf.ini']},
    include_package_data=True,
    zip_safe=False,
)
