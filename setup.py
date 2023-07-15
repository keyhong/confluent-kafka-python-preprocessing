#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

try:
    exec(open("preprocessing/_version.py").read())
except IOError:
    print(
        "Failed to load PySpark version file for packaging. You must be in preprocessing's python dir.",
        file=sys.stderr,
    )
    sys.exit(-1)

VERSION = __version__

with open("README.rst") as f:
    long_description = f.read()

if __name__ == "__main__":
    
    setup(
        name="perprocessing",
        version=VERSION,
        description='Confluent-Kafka-Python Preprocessing Program',
        long_description=long_description,
        author="Gyuwon Hong",
        author_email="wnhong96@gmail.com",
        license="Apache License",
        packages=find_packages(),
        install_requires=[
            "numpy",
            "pandas",
            "scikit-learn",
            "confluent-kafka==2.1.1",
        ],
        python_requires=">=3.6"
    )