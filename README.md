pytest-ordering
===============

pytest plugin to run your tests in a specific order

[![Build Status](https://travis-ci.org/ftobia/pytest-ordering.svg?branch=develop)](https://travis-ci.org/ftobia/pytest-ordering)

Have you ever wanted to easily run one of your tests before any others run?
Or run some tests last? Or run this one test before that other test? Or
make sure that this group of tests runs after this other group of tests?

Now you can.

Install with:

    pip install pytest-ordering

This defines some pytest markers that you can use in your code.

For example, this:

    import pytest

    @pytest.mark.run(order=2)
    def test_foo():
        assert True

    @pytest.mark.run(order=1)
    def test_bar():
        assert True

Yields this output:

    $ py.test test_foo.py -vv
    ============================= test session starts ==============================
    platform darwin -- Python 2.7.5 -- py-1.4.20 -- pytest-2.5.2 -- env/bin/python
    plugins: ordering
    collected 2 items

    test_foo.py:7: test_bar PASSED
    test_foo.py:3: test_foo PASSED

    =========================== 2 passed in 0.01 seconds ===========================

Check out the docs: http://pytest-ordering.readthedocs.org/
