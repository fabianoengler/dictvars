import re
from setuptools import setup
from pathlib import Path


mainpkg = 'dictvars'


def read_file(fname):
    return open(str(fname), 'rt').read()


def read_version():
    content = read_file(Path(mainpkg) / '__init__.py')
    return re.search(r"__version__ = '([^']+)'", content).group(1)


setup(
    name=mainpkg,
    version=read_version(),
    description='Create dicts from variables in scope',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Fabiano Engler',
    author_email='fabianoengler@gmail.com',
    url='https://github.com/fabianoengler/dictvars',
    packages=[mainpkg],
    )
