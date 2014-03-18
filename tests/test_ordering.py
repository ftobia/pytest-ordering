import operator
import os
import random
import re

import pytest

from pytest_ordering import _order_tests

__here__ = os.path.dirname(os.path.abspath(__file__))


def get_module(module_name):
    return __import__(module_name, globals(), locals(), [], -1)


def get_tests(module_name):
    module = get_module(module_name)
    return [getattr(module, t) for t in dir(module) if t.startswith('test_')]


def _names_of_tests(output, test_file_name):
    regex = r'^{0}:(\d+): test_([a-z]) PASSED$'.format(
        test_file_name.replace('.', '\.'))
    for line in output.split('\n'):
        match = re.match(regex, line)
        if match:
            yield match.group(2)


def get_order(output, test_file_name):
    return list(_names_of_tests(output, test_file_name))


# Default sorting is whatever order the tests show up in the module.

@pytest.mark.parametrize('module_name', [
    'numbers', 'words', 'words_backwards',
    # 'grouping', # This one is going to be tricky.
])
def test_ordering(module_name, capsys):
    module = get_module(module_name)
    pytest.main('{0}/{1}.py -vv'.format(__here__, module_name))
    relative_filename = 'tests/{0}.py'.format(module_name)
    out, err = capsys.readouterr()
    assert list(module.ordering) == get_order(out, relative_filename)
