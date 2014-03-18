#!/usr/bin/env python

from setuptools import setup


setup(
    name='pytest-ordering',
    description='pytest plugin to run your tests in a specific order',
    version='0.1',
    author='Frank Tobia',
    author_email='frank.tobia@gmail.com',
    url='https://github.com/ftobia/pytest-ordering',
    py_modules=['pytest_ordering'],
    entry_points = {
        'pytest11': [
            'pytest_ordering = pytest_ordering',
        ]
    },
    install_requires=['pytest'],
)
