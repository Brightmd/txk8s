# txk8s

A Twisted implementation of Kubernetes

## For maintainers: How to build

1. Increment `__version__` in `__version.py`.
2. Update the Change Log below.
3. Run the following:

```
python setup.py sdist bdist_wheel
twine upload dist/*<version>*
```

## Change Log
### [0.0.1] - 2017-12-21
#### Changed
- v1 yo
