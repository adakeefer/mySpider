# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name="pyspider",
    version="0.1.0",
    description="Python web crawler",
    url="https://github.com/adakeefer/threeSpiders",
    author="Adam Keefer",
    author_email="adamjkeefer@gmail.com",
    package_dir={"": "spider"},
    packages=find_packages(where="spider"),
    python_requires=">=3.7, <4",
    install_requires=[],
)
