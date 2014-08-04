import re

import pytest

import pytest_ordering
from . import numbers, words, words_backwards, grouping, custom_groups


@pytest.mark.parametrize('module', [
    numbers, words, words_backwards, grouping, custom_groups,
])
def test_ordered_tests(module, testdir):
    items = testdir.getitems(module)
    ordered_tests = list(pytest_ordering._order_tests(items))
    ordered_letters = [item.name[-1] for item in ordered_tests]
    assert ordered_letters == list(module.ordering)


def test_run_marker_registered(capsys):
    pytest.main('--markers')
    out, err = capsys.readouterr()
    assert '@pytest.mark.run' in out


def test_version():
    assert hasattr(pytest_ordering, '__version__')
    assert re.match(r'[0-9]+\.[0-9]+(\.[0-9]+)?$', pytest_ordering.__version__)
