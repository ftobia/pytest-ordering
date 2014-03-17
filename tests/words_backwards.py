import pytest

ordering = 'dgfbcae'


@pytest.mark.second_to_last
def test_a():
    pass


@pytest.mark.fourth_to_last
def test_b():
    pass


@pytest.mark.third_to_last
def test_c():
    pass


@pytest.mark.seventh_to_last
def test_d():
    pass


@pytest.mark.last
def test_e():
    pass


@pytest.mark.fifth_to_last
def test_f():
    pass


@pytest.mark.sixth_to_last
def test_g():
    pass
