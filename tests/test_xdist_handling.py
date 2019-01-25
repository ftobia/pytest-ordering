# -*- coding: utf-8 -*-

import pytest
import pytest_ordering

pytest_plugins = ['pytester']


def test_xdist_ordering(tmpdir):
    testname = str(tmpdir.join("first_test.py"))
    with open(testname, "w") as fi:
        fi.write(
            """
import pytest

val = 1

@pytest.mark.second
def test_second_integer():
    global val
    assert val == 2
    val += 1

def test_last_integer():
    assert val == 3

@pytest.mark.first
def test_first_integer():
    global val
    assert val == 1
    val += 1
"""
        )

    testname = str(tmpdir.join("second_test.py"))
    with open(testname, "w") as fi:
        fi.write(
            """
import pytest

val = "frog"

@pytest.mark.second
def test_second_string():
    global val
    assert val == "goat"
    val = "fish"

def test_last_string():
    assert val == "fish"

@pytest.mark.first
def test_first_string():
    global val
    assert val == "frog"
    val = "goat"
"""
        )
    # With `loadfile`, the tests should pass
    args = ["-n3", "--dist=loadfile", str(tmpdir)]
    ret = pytest.main(args, [pytest_ordering])
    assert ret == 0

    # Without `loadfile`, the tests should fail
    args = ["-n3", str(tmpdir)]
    ret = pytest.main(args, [pytest_ordering])
    assert ret == 1
