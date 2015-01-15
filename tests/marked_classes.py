import pytest

ordering = 'fdeabc'


@pytest.mark.order3
class TestA:
    def test_a():
        pass

    def test_b():
        pass

    def test_c():
        pass


@pytest.mark.order2
class TestB:
    def test_d():
        pass

    def test_e():
        pass


@pytest.mark.order1
def test_f():
    pass
