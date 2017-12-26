from setuptools import setup
from inspect import cleandoc


_version = {}
execfile('txk8s/_version.py', _version)

setup(
  name = 'txk8s',
  packages = ['txk8s', 'txk8s.test'],
  version = _version['__version__'],
  description = 'A Twisted implementation of Kubernetes',
  author = 'Jessica Grebenschikov',
  author_email = 'jessica@bright.md',
  url = 'https://github.com/Brightmd/txk8s',
  keywords = ['twisted', 'kubernetes'],
  classifiers = [],
  scripts = [],
  install_requires=cleandoc('''
    kubernetes>=3.0.0,<3.1.0
    Twisted>=16.0.0,<18.0.0
    PyYAML>=3.10,<4.0.0
    ''').split()
)
