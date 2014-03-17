import pytest

ordering = 'fcbaged'


@pytest.mark.order4
def test_a():
    pass


@pytest.mark.order3
def test_b():
    pass


@pytest.mark.order2
def test_c():
    pass


@pytest.mark.order7
def test_d():
    pass


@pytest.mark.order6
def test_e():
    pass


@pytest.mark.order1
def test_f():
    pass


@pytest.mark.order5
def test_g():
    pass
