#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re
import ast
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'raiblocks'
DESCRIPTION = 'RaiBlocks Python RPC client for rai_node'
URL = 'https://github.com/dourvaris/raiblocks-python'
EMAIL = 'dourvaris@gmail.com'
AUTHOR = 'Daniel Dourvaris'

with open('requirements.pip') as f:
    INSTALL_REQUIRES = f.read().splitlines()

with open('requirements-dev.pip') as f:
    TESTS_REQUIRE = f.read().splitlines()

here = os.path.abspath(os.path.dirname(__file__))


with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open(os.path.join(here, NAME, 'version.py'), 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()

setup(
    name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    py_modules=[NAME],
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    setup_requires=['pytest-runner'],
    include_package_data=True,
    packages=find_packages(exclude=('tests*',)),
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Development Status :: 3 - Alpha'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)