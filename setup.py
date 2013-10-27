from distutils.core import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
import sys

PACKAGE = "litefac_launchpad"
NAME = "litefac-launchpad"
DESCRIPTION = "Launchpad for litefac"
AUTHOR = "XieChao"
AUTHOR_EMAIL = "xiechao06@gmail.com"
URL = "xiechao06.github.com"
VERSION = '0.9.0-dev'
DOC = __doc__


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name=NAME,
    version=VERSION,
    long_description=__doc__,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    install_requires=open('requirements.txt').readlines(),
)
