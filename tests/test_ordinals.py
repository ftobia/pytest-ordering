import pytest

@pytest.mark.run('second_to_last')
def test_three():
    assert True

@pytest.mark.run('last')
def test_four():
    assert True

@pytest.mark.run('second')
def test_two():
    assert True

@pytest.mark.run('first')
def test_one():
    assert True