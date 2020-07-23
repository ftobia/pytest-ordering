# -*- coding: utf-8 -*-
import re
import warnings

import pytest

pytest_plugins = ['pytester']


@pytest.fixture
def item_names_for(testdir):

    def _item_names_for(tests_content):
        # some strange code to extract sorted items
        items = testdir.getitems(tests_content)
        hook = testdir.config.hook
        hook.pytest_collection_modifyitems(session=items[0].session,
                                           config=testdir.config, items=items)
        return [item.name for item in items]

    return _item_names_for


def test_no_marks(item_names_for):
    tests_content = """
    def test_1(): pass

    def test_2(): pass
    """

    assert item_names_for(tests_content) == ['test_1', 'test_2']


def test_first_mark(item_names_for):
    tests_content = """
    import pytest

    def test_1(): pass

    @pytest.mark.first
    def test_2(): pass
    """

    assert item_names_for(tests_content) == ['test_2', 'test_1']


def test_last_mark(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.last
    def test_1(): pass

    def test_2(): pass
    """

    assert item_names_for(tests_content) == ['test_2', 'test_1']


def test_first_last_marks(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.last
    def test_1(): pass

    @pytest.mark.first
    def test_2(): pass

    def test_3(): pass
    """

    assert item_names_for(tests_content) == ['test_2', 'test_3', 'test_1']


def test_order_marks(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.run(order=-1)
    def test_1(): pass

    @pytest.mark.run(order=-2)
    def test_2(): pass

    @pytest.mark.run(order=1)
    def test_3(): pass
    """

    assert item_names_for(tests_content) == ['test_3', 'test_2', 'test_1']


def test_non_contiguous_positive(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.run(order=10)
    def test_1(): pass

    @pytest.mark.run(order=20)
    def test_2(): pass

    @pytest.mark.run(order=5)
    def test_3(): pass
    """

    assert item_names_for(tests_content) == ['test_3', 'test_1', 'test_2']


def test_non_contiguous_negative(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.run(order=-10)
    def test_1(): pass

    @pytest.mark.run(order=-20)
    def test_2(): pass

    @pytest.mark.run(order=-5)
    def test_3(): pass
    """

    assert item_names_for(tests_content) == ['test_2', 'test_1', 'test_3']


def test_non_contiguous_inc_zero(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.run(order=10)
    def test_1(): pass

    @pytest.mark.run(order=20)
    def test_2(): pass

    @pytest.mark.run(order=5)
    def test_3(): pass

    @pytest.mark.run(order=-10)
    def test_4(): pass

    @pytest.mark.run(order=-20)
    def test_5(): pass

    @pytest.mark.run(order=-5)
    def test_6(): pass

    @pytest.mark.run(order=0)
    def test_7(): pass
    """

    assert item_names_for(tests_content) == ['test_7', 'test_3', 'test_1', 'test_2', 'test_5', 'test_4', 'test_6']


def test_non_contiguous_inc_none(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.run(order=5)
    def test_1(): pass

    @pytest.mark.run(order=0)
    def test_2(): pass

    @pytest.mark.run(order=1)
    def test_3(): pass

    @pytest.mark.run(order=-1)
    def test_4(): pass

    @pytest.mark.run(order=-5)
    def test_5(): pass

    def test_6(): pass
    """

    assert item_names_for(tests_content) == ['test_2', 'test_3', 'test_1', 'test_6', 'test_5', 'test_4']


def test_first_mark_class(item_names_for):
    tests_content = """
    import pytest

    def test_1(): pass


    @pytest.mark.first
    class TestSuite(object):

        def test_3(self): pass

        def test_2(self): pass

    """

    assert item_names_for(tests_content) == ['test_3', 'test_2', 'test_1']


def test_last_mark_class(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.last
    class TestSuite(object):

        def test_1(self): pass

        def test_2(self): pass


    def test_3(): pass
    """

    assert item_names_for(tests_content) == ['test_3', 'test_1', 'test_2']


def test_first_last_mark_class(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.last
    class TestLast(object):

        def test_1(self): pass

        def test_2(self): pass


    def test_3(): pass


    @pytest.mark.first
    class TestFirst(object):

        def test_4(self): pass

        def test_5(self): pass

    """

    assert item_names_for(tests_content) == ['test_4', 'test_5', 'test_3', 'test_1', 'test_2']


def test_order_mark_class(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.run(order=-1)
    class TestLast(object):

        def test_1(self): pass

        def test_2(self): pass


    @pytest.mark.run(order=0)
    def test_3(): pass


    @pytest.mark.run(order=-2)
    class TestFirst(object):

        def test_4(self): pass

        def test_5(self): pass
    """

    assert item_names_for(tests_content) == ['test_3', 'test_4', 'test_5', 'test_1', 'test_2']


def test_relative_to_other_tests(item_names_for):
    tests_content = """
    import pytest
    
    @pytest.mark.run(after='test_2')
    def test_3(): pass

    def test_2(): pass

    @pytest.mark.run(before='test_2')
    def test_1(): pass
    """
    assert item_names_for(tests_content) == ['test_1', 'test_2', 'test_3']

def test_relative_to_other_invalid_tests(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.run(before='test_A')
    def test_1(): pass

    def test_2(): pass
    
    @pytest.mark.run(after='test_B')
    def test_3(): pass
    
    @pytest.mark.run(before='test_C')
    def test_4(): pass
    
    @pytest.mark.run(before='test_C')
    def test_5(): pass
    
    @pytest.mark.run(before='test_C')
    def test_6(): pass
    
    @pytest.mark.run(after='test_D')
    def test_7(): pass
    
    @pytest.mark.run(after='test_D')
    def test_8(): pass
    """
    
    with warnings.catch_warnings(record=True) as catched_warnings:
        assert item_names_for(tests_content) == [
            'test_2', 'test_1', 'test_4', 'test_5',
            'test_6', 'test_3', 'test_7', 'test_8',
        ]
        
        expected_warning_messages = [
            "test_A, indicated at parameter before of test_1, doesn't exist",
            "test_B, indicated at parameter after of test_3, doesn't exist",
            "test_C, indicated at parameter before of test_4, test_5 and test_6, doesn't exist",
            "test_D, indicated at parameter after of test_7 and test_8, doesn't exist",
        ]
        
        n_other_warnings = 0        
        for w in catched_warnings:
            if not issubclass(w.category, SyntaxWarning):
                n_other_warnings += 1
                continue
            assert w.message.__str__() in expected_warning_messages
        assert len(expected_warning_messages) + n_other_warnings == len(catched_warnings)


def test_markers_registered(capsys):
    pytest.main(['--markers'])
    out, err = capsys.readouterr()
    assert '@pytest.mark.run' in out
    assert '@pytest.mark.first' in out
    assert '@pytest.mark.last' in out
    assert out.count('Provided by pytest-ordering') == 17
