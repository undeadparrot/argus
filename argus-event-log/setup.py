from setuptools import setup

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f]

setup(
    install_requires=requirements
)
