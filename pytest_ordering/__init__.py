# -*- coding: utf-8 -*-
from ._version import __version__

import pytest

orders_map = {
    'first': 0,
    'second': 1,
    'third': 2,
    'fourth': 3,
    'fifth': 4,
    'sixth': 5,
    'seventh': 6,
    'eighth': 7,
    'last': -1,
    'second_to_last': -2,
    'third_to_last': -3,
    'fourth_to_last': -4,
    'fifth_to_last': -5,
    'sixth_to_last': -6,
    'seventh_to_last': -7,
    'eighth_to_last': -8,
}


def pytest_configure(config):
    """Register the "run" marker."""

    config_line = (
        'run: specify ordering information for when tests should run '
        'in relation to one another. Provided by pytest-ordering. '
        'See also: http://pytest-ordering.readthedocs.org/'
    )
    config.addinivalue_line('markers', config_line)


def pytest_collection_modifyitems(session, config, items):
    grouped_items = {}

    for item in items:

        for mark_name, order in orders_map.items():
            mark = item.get_marker(mark_name)

            if mark:
                item.add_marker(pytest.mark.run(order=order))
                break

        mark = item.get_marker('run')

        if mark:
            order = mark.kwargs.get('order')
        else:
            order = None

        grouped_items.setdefault(order, []).append(item)

    if grouped_items:
        unordered_items = grouped_items.pop(None, None)

        sorted_items = []
        prev_key = 0

        for key, ordered_items in grouped_items.items():

            if unordered_items and prev_key >= 0 and key < 0:

                sorted_items.extend(unordered_items)
                unordered_items = None

            prev_key = key

            sorted_items.extend(ordered_items)

        if unordered_items:
            sorted_items.extend(unordered_items)

        items[:] = sorted_items
