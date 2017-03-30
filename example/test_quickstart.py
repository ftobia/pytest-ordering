import pytest

@pytest.mark.order2
def test_foo():
    assert True

@pytest.mark.order1
def test_bar():
    assert True