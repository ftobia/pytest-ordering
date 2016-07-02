# -*- coding: utf-8 -*-


def test_first(item_names_for):
    tests_content = """
    import pytest

    def test_1(): pass

    @pytest.mark.first
    def test_2(): pass
    """
    assert item_names_for(tests_content) == ['test_2', 'test_1']


def test_second(item_names_for):
    tests_content = """
    import pytest

    def test_1(): pass
    def test_2(): pass
    def test_3(): pass
    def test_4(): pass

    @pytest.mark.second
    def test_5(): pass
    """
    assert item_names_for(tests_content) == ['test_1', 'test_5', 'test_2', 'test_3', 'test_4']


def test_third(item_names_for):
    tests_content = """
    import pytest

    def test_1(): pass
    def test_2(): pass
    def test_3(): pass

    @pytest.mark.third
    def test_4(): pass

    def test_5(): pass
    """
    assert item_names_for(tests_content) == ['test_1', 'test_2', 'test_4', 'test_3', 'test_5']


def test_second_to_last(item_names_for):
    tests_content = """
    import pytest

    def test_1(): pass

    @pytest.mark.second_to_last
    def test_2(): pass

    def test_3(): pass
    def test_4(): pass
    def test_5(): pass
    """
    assert item_names_for(tests_content) == ['test_1', 'test_3', 'test_4', 'test_2', 'test_5']


def test_last(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.last
    def test_1(): pass

    def test_2(): pass
    """
    assert item_names_for(tests_content) == ['test_2', 'test_1']


def test_first_last(item_names_for):
    tests_content = """
    import pytest

    @pytest.mark.last
    def test_1(): pass

    @pytest.mark.first
    def test_2(): pass

    def test_3(): pass
    """
    assert item_names_for(tests_content) == ['test_2', 'test_3', 'test_1']
