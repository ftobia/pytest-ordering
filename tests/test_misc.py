# -*- coding: utf-8 -*-
import re

import pytest
import pytest_ordering


def test_version_exists():
    assert hasattr(pytest_ordering, '__version__')


def test_version_valid():
    assert re.match(r'[0-9]+\.[0-9]+(\.[0-9]+)?$',
                    pytest_ordering.__version__)


def test_run_marker_registered(capsys):
    pytest.main('--markers')
    out, err = capsys.readouterr()
    assert '@pytest.mark.run' in out
