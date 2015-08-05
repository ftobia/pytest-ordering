#!/usr/bin/env python

from setuptools import setup
import os

__here__ = os.path.abspath(os.path.dirname(__file__))

# define __version__
# execfile doesn't exist in python 3
# see: http://stackoverflow.com/questions/6357361/alternative-to-execfile-in-python-3-2
exec(open(os.path.join(__here__, 'pytest_ordering', '_version.py')).read())


setup(
    name='pytest-ordering',
    description='pytest plugin to run your tests in a specific order',
    version=__version__,
    author='Frank Tobia',
    author_email='frank.tobia@gmail.com',
    url='https://github.com/ftobia/pytest-ordering',
    packages=['pytest_ordering'],
    entry_points = {
        'pytest11': [
            'pytest_ordering = pytest_ordering',
        ]
    },
    install_requires=['pytest'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
