import pytest

ordering = 'agbdicfhjke'


@pytest.mark.custom_group1
def test_a():
    pass


@pytest.mark.custom_group3
def test_b():
    pass


@pytest.mark.custom_group6
def test_c():
    pass


@pytest.mark.custom_group4
def test_d():
    pass


@pytest.mark.custom_group11
def test_e():
    pass


@pytest.mark.custom_group7
def test_f():
    pass


@pytest.mark.custom_group2
def test_g():
    pass


@pytest.mark.custom_group8
def test_h():
    pass


@pytest.mark.custom_group5
def test_i():
    pass


@pytest.mark.custom_group9
def test_j():
    pass


@pytest.mark.custom_group10
def test_k():
    pass
