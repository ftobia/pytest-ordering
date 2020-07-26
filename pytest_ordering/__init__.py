# -*- coding: utf-8 -*-
from ._version import __version__

import operator

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

    provided_by_pytest_ordering = (
        'Provided by pytest-ordering. '
        'See also: http://pytest-ordering.readthedocs.org/'
    )

    config_line = (
        'run: specify ordering information for when tests should run '
        'in relation to one another. ' + provided_by_pytest_ordering
    )
    config.addinivalue_line('markers', config_line)

    for mark_name in orders_map.keys():
        config_line = '{}: run test {}. {}'.format(mark_name,
                                                   mark_name.replace('_', ' '),
                                                   provided_by_pytest_ordering)
        config.addinivalue_line('markers', config_line)


def pytest_collection_modifyitems(session, config, items):
    grouped_items = {}

    for item in items:

        for mark_name, order in orders_map.items():
            mark = item.get_closest_marker(mark_name)

            if mark:
                item.add_marker(pytest.mark.run(order=order))
                break

        mark = item.get_closest_marker('run')

        if mark:
            order = mark.kwargs.get('order')
        else:
            order = None

        grouped_items.setdefault(order, []).append(item)

    sorted_items = []
    unordered_items = grouped_items.pop(None, [])

    start_list = sorted((i for i in grouped_items.items() if i[0] >= 0),
                        key=operator.itemgetter(0))

    index = 0
    for i, item_list in start_list:
        while i > index and unordered_items:
            sorted_items.append(unordered_items.pop(0))
            index += 1
        sorted_items.extend(item_list)
        index += len(item_list)

    end_list = reversed(sorted((i for i in grouped_items.items() if i[0] < 0),
                               key=operator.itemgetter(0)))
    index = -1
    sorted_end_list = []
    for i, item_list in end_list:
        while i < index and unordered_items:
            sorted_end_list.append(unordered_items.pop())
            index -= 1
        sorted_end_list.extend(reversed(item_list))
        index -= len(item_list)

    sorted_items.extend(unordered_items)
    sorted_items.extend(reversed(sorted_end_list))
    items[:] = sorted_items
