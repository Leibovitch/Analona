from setuptools import setup, find_packages

import analona

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name=analona.__name__,
    author="NSPLT",
    description="Analytics Validation scheme",
    keywords="schema json validation",
    url="https://github.com/nsplt/Analona",
    packages=find_packages(),
    py_modules=['analona'],
    long_description=open('README.md').read(),
    install_requires=requirements,
)
