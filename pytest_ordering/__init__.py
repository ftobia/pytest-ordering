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


def get_markerrun_scope_and_order(item):
    mark = item.get_marker('run')
    if mark:
        scope = mark.kwargs.get('scope')
        order = mark.kwargs.get('order')
    else:
        scope = None
        order = None
    return scope, order


def order_grouped_items(grouped_items):
    '''grouped_items is a dict of form {1:[], 2:[], 3:[]..}'''

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

    return sorted_items


def group_class_items_by_order(items):
    '''orders only the items which belog to scope class'''
    grouped_items = {}

    for item in items:  
        scope, order = get_markerrun_scope_and_order(item)

        if scope == 'class' and order is None:
            raise Exception("order attribute not provided in marker for test %s" % item.name)
        elif scope is None:
            # ignoring items whose scope is not defined
            grouped_items.setdefault(None, []).append(item)
        else:
            grouped_items.setdefault(order, []).append(item)

    if grouped_items:
        return order_grouped_items(grouped_items)
    return items
    

def pytest_collection_modifyitems(session, config, items):
    grouped_items = {}

    items_cls = []
    prev_cls = None
    current_cls = None

    for item in items:  
        for mark_name, order in orders_map.items():
            mark = item.get_marker(mark_name)

            if mark:
                item.add_marker(pytest.mark.run(order=order))
                break

        scope, order = get_markerrun_scope_and_order(item)

        current_cls = item.cls

        if prev_cls is None and current_cls:
            items_cls[:] = [item]
        elif prev_cls is not None and prev_cls == current_cls:
            items_cls.append(item)
        elif prev_cls is not None and prev_cls != current_cls:
            # arranging the items of same class i.e. items_cls and adding to grouped_items
            for elem in group_class_items_by_order(items_cls):
                elem_scope, elem_order = get_markerrun_scope_and_order(item)

                if elem_scope == 'class':
                    # ignoring items whose scope is defined as its already processed
                    grouped_items.setdefault(None, []).append(elem)
                else:
                    grouped_items.setdefault(elem_order, []).append(elem)
            items_cls[:] = [item]
        else:
            grouped_items.setdefault(order, []).append(item)

        prev_cls = current_cls

    else:
        # arranging the items of same class i.e. items_cls and adding to grouped_items
        for elem in group_class_items_by_order(items_cls):
            elem_scope, elem_order = get_markerrun_scope_and_order(item)

            if elem_scope == 'class':
                # ignoring items whose scope is defined as its already processed
                grouped_items.setdefault(None, []).append(elem)
            else:
                grouped_items.setdefault(elem_order, []).append(elem)

    if grouped_items:
        items[:] = order_grouped_items(grouped_items)
