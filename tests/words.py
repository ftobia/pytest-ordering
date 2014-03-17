import pytest

ordering = 'dabgfce'


@pytest.mark.second
def test_a():
    pass


@pytest.mark.third
def test_b():
    pass


@pytest.mark.sixth
def test_c():
    pass


@pytest.mark.first
def test_d():
    pass


@pytest.mark.seventh
def test_e():
    pass


@pytest.mark.fifth
def test_f():
    pass


@pytest.mark.fourth
def test_g():
    pass
