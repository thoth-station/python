#!/usr/bin/env python3

import os
from setuptools import setup
from pathlib import Path


def get_requirements():
    with open('requirements.txt') as fd:
        return fd.read().splitlines()


def get_version():
    with open(os.path.join('thoth', 'python', '__init__.py')) as f:
        content = f.readlines()

    for line in content:
        if line.startswith('__version__ ='):
            # dirty, remove trailing and leading chars
            return line.split(' = ')[1][1:-2]

    raise ValueError("No package version found")


setup(
    name='thoth-python',
    version=get_version(),
    packages=[
        'thoth.python'
    ],
    install_requires=get_requirements(),
    author='Fridolin Pokorny',
    author_email='fridolin@redhat.com',
    maintainer='Fridolin Pokorny',
    maintainer_email='fridolin@redhat.com',
    description='A Python ecosystem specific library',
    long_description=Path('README.rst').read_text(),
    url='https://github.com/thoth-station/python',
    license='GPLv3+',
    keywords='python dependency pypi dependencies tool library thoth',
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: CPython",
    ]
)
