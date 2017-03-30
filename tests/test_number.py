import pytest

@pytest.mark.run(order=-2)
def test_three():
    assert True

@pytest.mark.run(order=-1)
def test_four():
    assert True

@pytest.mark.run(order=2)
def test_two():
    assert True

@pytest.mark.run(order=1)
def test_one():
    assert True