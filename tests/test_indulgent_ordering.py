# -*- coding: utf-8 -*-
import re

import pytest
import pytest_ordering

pytest_plugins = ["pytester"]


def test_run_marker_registered(capsys, tmpdir):
    testname = str(tmpdir.join("failing.py"))
    with open(testname, "w") as fi:
        fi.write(
            """
import pytest

@pytest.mark.second
def test_me_second():
    assert True

def test_that_fails():
    assert False

@pytest.mark.first
def test_me_first():
    assert True
"""
        )
    args = ["--quiet", "--color=no", testname]
    pytest.main(args, [pytest_ordering])
    out, err = capsys.readouterr()
    assert "..F" in out
    args.insert(0, "--ff")
    pytest.main(args, [pytest_ordering])
    out, err = capsys.readouterr()
    assert "..F" in out
    args.insert(0, "--indulgent-ordering")
    pytest.main(args, [pytest_ordering])
    out, err = capsys.readouterr()
    assert "F.." in out
