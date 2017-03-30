import pytest

@pytest.mark.second_to_last
def test_three():
    assert True

@pytest.mark.last
def test_four():
    assert True

@pytest.mark.second
def test_two():
    assert True

@pytest.mark.first
def test_one():
    assert True