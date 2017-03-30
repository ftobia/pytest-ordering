import pytest

@pytest.mark.run(after='test_second')
def test_third():
    assert True

def test_second():
    assert True

@pytest.mark.run(before='test_second')
def test_first():
    assert True