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
    """Register the "run" marker and configur the plugin depending on the CLI
    options"""

    config_line = (
        'run: specify ordering information for when tests should run '
        'in relation to one another. Provided by pytest-ordering. '
        'See also: http://pytest-ordering.readthedocs.org/'
    )
    config.addinivalue_line('markers', config_line)
    if config.getoption('indulgent-ordering'):
        # We need to dynamically add this `tryfirst` decorator to the plugin:
        # only when the CLI option is present should the decorator be added.
        # Thus, we manually run the decorator on the class function and
        # manually replace it.
        # Python 2.7 didn't allow arbitrary attributes on methods, so we have
        # to keep the function as a function and then add it to the class as a
        # pseudomethod.  Since the class is purely for structuring and `self`
        # is never referenced, this seems reasonable.
        OrderingPlugin.pytest_collection_modifyitems = pytest.hookimpl(
                function=modify_items, tryfirst=True)
    else:
        OrderingPlugin.pytest_collection_modifyitems = pytest.hookimpl(
                function=modify_items, trylast=True)
    config.pluginmanager.register(OrderingPlugin(), 'orderingplugin')


def pytest_addoption(parser):
    """Set up CLI option for pytest"""
    group = parser.getgroup('ordering')
    group.addoption('--indulgent-ordering', action='store_true',
                     dest='indulgent-ordering', help='''Request that the sort \
order provided by pytest-ordering be applied before other sorting, allowing the \
other sorting to have priority''')

class OrderingPlugin:
    """
    Plugin implementation

    By putting this in a class, we are able to dynamically register it after
    the CLI is parsed.
    """

def modify_items(session, config, items):
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
    unordered_items = [grouped_items.pop(None, [])]

    start_list = sorted((i for i in grouped_items.items() if i[0] >= 0),
                        key=operator.itemgetter(0))
    end_list = sorted((i for i in grouped_items.items() if i[0] < 0),
                      key=operator.itemgetter(0))

    sorted_items.extend([i[1] for i in start_list])
    sorted_items.extend(unordered_items)
    sorted_items.extend([i[1] for i in end_list])

    items[:] = [item for sublist in sorted_items for item in sublist]
