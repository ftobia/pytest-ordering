.. pytest-ordering documentation master file, created by
   sphinx-quickstart on Mon Mar 17 18:20:44 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pytest-ordering: pytest plugin to run your tests in a specific order
====================================================================

pytest-ordering provides custom markers_ that let you run your tests
in any order you would like.

Ordinarily pytest will run tests in the order that they appear in a module.
For example, for the following tests:

.. code:: python

 def test_foo():
     assert True

 def test_bar():
     assert True

Here is the output:

::

    $ py.test test_foo.py -vv
    ============================= test session starts ==============================
    platform darwin -- Python 2.7.5 -- py-1.4.20 -- pytest-2.5.2 -- env/bin/python
    collected 2 items

    test_foo.py:2: test_foo PASSED
    test_foo.py:6: test_bar PASSED

    =========================== 2 passed in 0.01 seconds ===========================

With pytest-ordering, you can change the default ordering as follows:

.. code:: python

 import pytest

 @pytest.mark.order2
 def test_foo():
     assert True

 @pytest.mark.order1
 def test_bar():
     assert True

::

    $ py.test test_foo.py -vv
    ============================= test session starts ==============================
    platform darwin -- Python 2.7.5 -- py-1.4.20 -- pytest-2.5.2 -- env/bin/python
    plugins: ordering
    collected 2 items

    test_foo.py:7: test_bar PASSED
    test_foo.py:3: test_foo PASSED

    =========================== 2 passed in 0.01 seconds ===========================

This is a trivial example, but ordering is respected across test files.

You can also use markers such as "first", "second", "last", and "second_to_last":

.. code:: python

 import pytest

 @pytest.mark.second_to_last
 def test_three():
     assert True

 @pytest.mark.last
 def test_four():
     assert True

 @pytest.mark.second
 def test_two():
     assert True

 @pytest.mark.first
 def test_one():
     assert True

::

    $ py.test test_foo.py -vv
    ============================= test session starts ==============================
    platform darwin -- Python 2.7.5 -- py-1.4.20 -- pytest-2.5.2 -- env/bin/python
    plugins: ordering
    collected 4 items

    test_foo.py:17: test_one PASSED
    test_foo.py:12: test_two PASSED
    test_foo.py:3: test_three PASSED
    test_foo.py:7: test_four PASSED

    =========================== 4 passed in 0.02 seconds ===========================




.. toctree::
   :maxdepth: 2

.. _markers: https://pytest.org/latest/mark.html

