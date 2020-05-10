# -*- coding: utf-8 -*-
"""Setup file for dobot_magician_utilities.
"""

from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="dobot_magician_utilities",
    version="0.0.1dev",
    description="Utility programs for the dobot magician robotic arm, written in python. Useful for setting up experiments",
    license="GPLv3",
    long_description=long_description,
    author="Ben Money-Coomes",
    author_email="ben.money@gmail.com",
    url="https://github.com/meisben",
    packages=["dobot_magician_utilities", ],
    install_requires=["numpy", "pandas"]
)
