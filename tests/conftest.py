import pytest


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

