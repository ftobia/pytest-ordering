# -*- coding: utf-8 -*-

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
