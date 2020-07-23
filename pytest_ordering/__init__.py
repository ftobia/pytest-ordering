# -*- coding: utf-8 -*-
from ._version import __version__

import operator
import warnings

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
    grouped_items, before_items, after_items = ({}, {}, {})

    for item in items:

        for mark_name, order in orders_map.items():
            mark = item.get_closest_marker(mark_name)

            if mark:
                item.add_marker(pytest.mark.run(order=order))
                break

        mark = item.get_closest_marker('run')

        if mark:
            order = mark.kwargs.get('order')
            if order is None:
                before = mark.kwargs.get('before')
                if before:
                    before_items.setdefault(before, []).append(item)
                    continue
                
                after = mark.kwargs.get('after')
                if after:
                    after_items.setdefault(after, []).append(item)
                    continue
        else:
            order = None

        grouped_items.setdefault(order, []).append(item)

    sorted_items = []
    unordered_items = [grouped_items.pop(None, [])]

    start_list = sorted((i for i in grouped_items.items() if i[0] >= 0),
                        key=operator.itemgetter(0))
    end_list = sorted((i for i in grouped_items.items() if i[0] < 0),
                      key=operator.itemgetter(0))

    sorted_items.extend([i[1] for i in start_list])
    sorted_items.extend(unordered_items)
    sorted_items.extend([i[1] for i in end_list])

    items[:] = [item for sublist in sorted_items for item in sublist]
    
    def _get_item_index_by_name(item_name):
        index = None
        for i, item in enumerate(items):
            if getattr(item, 'name') == item_name:
                index = i
                break
        return index
        
    for before_item_relative, _before_items in before_items.items():
        index = _get_item_index_by_name(before_item_relative)
        if index is not None:
            for before_item in _before_items:
                items.insert(index, before_item)
        else:
            if len(_before_items) == 1:
                message_schema = "%s test, indicated at parameter before of" \
                               + " %s test, doesn't exists"
                message = message_schema % (before_item_relative,
                                            _before_items[0].name)
            else:
                message_schema = "%s test, indicated at parameter before of" \
                               + " %s tests, doesn't exists"
                test_names = ""
                for i, before_item in enumerate(_before_items):
                    test_names += before_item.name
                    if i < len(_before_items) - 2:
                        test_names += ", "
                    elif i == len(_before_items) - 2:
                        test_names += " and "
                message = message_schema % (before_item_relative, test_names)
            warnings.warn(message, SyntaxWarning)
            items.extend(_before_items)
    for after_item_relative, _after_items in after_items.items():
        index = _get_item_index_by_name(after_item_relative)
        if index is not None:
            for after_item in _after_items:
                items.insert(index+1, after_item)
        else:
            if len(_after_items) == 1:
                message_schema = "%s test, indicated at parameter after of" \
                               + " %s test, doesn't exists"
                message = message_schema % (after_item_relative,
                                            _after_items[0].name)
            else:
                message_schema = "%s test, indicated at parameter after of" \
                               + " %s tests, doesn't exists"
                test_names = ""
                for i, after_item in enumerate(_after_items):
                    test_names += after_item.name
                    if i < len(_after_items) - 2:
                        test_names += ", "
                    elif i == len(_after_items) - 2:
                        test_names += " and "
                message = message_schema % (after_item_relative, test_names)
            warnings.warn(message, SyntaxWarning)
            items.extend(_after_items)
