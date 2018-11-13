from setuptools import setup

import analona

setup(
    name=analona.__name__,
    version=analona.__version__,
    author="NSPLT",
    description="Analytics Validation scheme",
    keywords="schema json validation",
    url="https://github.com/nsplt/Analona",
    py_modules=['analona'],
    long_description=open('README.md').read(),
)