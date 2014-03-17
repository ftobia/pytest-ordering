import pytest

ordering = 'ckheofdvgwzyrulmbiqpjnxsta'


@pytest.mark.foo(order=25)
def test_a():
    pass


@pytest.mark.foo(order=16)
def test_b():
    pass


@pytest.mark.foo(order=0)
def test_c():
    pass


@pytest.mark.foo(order=6)
def test_d():
    pass


@pytest.mark.foo(order=3)
def test_e():
    pass


@pytest.mark.foo(order=5)
def test_f():
    pass


@pytest.mark.foo(order=8)
def test_g():
    pass


@pytest.mark.foo(order=2)
def test_h():
    pass


@pytest.mark.foo(order=17)
def test_i():
    pass


@pytest.mark.foo(order=20)
def test_j():
    pass


@pytest.mark.foo(order=1)
def test_k():
    pass


@pytest.mark.foo(order=14)
def test_l():
    pass


@pytest.mark.foo(order=15)
def test_m():
    pass


@pytest.mark.foo(order=21)
def test_n():
    pass


@pytest.mark.foo(order=4)
def test_o():
    pass


@pytest.mark.foo(order=19)
def test_p():
    pass


@pytest.mark.foo(order=18)
def test_q():
    pass


@pytest.mark.foo(order=12)
def test_r():
    pass


@pytest.mark.foo(order=23)
def test_s():
    pass


@pytest.mark.foo(order=24)
def test_t():
    pass


@pytest.mark.foo(order=13)
def test_u():
    pass


@pytest.mark.foo(order=7)
def test_v():
    pass


@pytest.mark.foo(order=9)
def test_w():
    pass


@pytest.mark.foo(order=22)
def test_x():
    pass


@pytest.mark.foo(order=11)
def test_y():
    pass


@pytest.mark.foo(order=10)
def test_z():
    pass
