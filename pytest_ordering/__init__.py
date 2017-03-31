# -*- coding: utf-8 -*-
from ._version import __version__

import operator
import re
import pytest
try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict
import os
import sys

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
    'eighth_to_last': -8
}


def pytest_configure(config):
    """Register the "run" marker."""

    config_line = (
        'run: specify ordering information for when tests should run '
        'in relation to one another. Provided by pytest-ordering. '
        'See also: http://pytest-ordering.readthedocs.org/'
    )
    config.addinivalue_line('markers', config_line)


def get_filename(item):
    name = item.location[0]
    if os.sep in name:
        name = item.location[0].rsplit(os.sep, 1)[1]
    return name[:-3]


def mark_binning(item, keys, start, end, before, after, unordered):
    match_order = re.compile(r"order(\d+)(:?,|$)")
    find_order = match_order.search(",".join(keys))
    if find_order:
        order = int(find_order.group(1))
        start.setdefault(order, []).append(item)
        return True
    elif "run" in keys:
        mark = item.get_marker('run')
        order = mark.kwargs.get('order')
        before_mark = mark.kwargs.get('before')
        after_mark = mark.kwargs.get('after')
        if order is not None:
            order = int(order)
            if order < 0:
                end.setdefault(order, []).append(item)
            else:
                start.setdefault(order, []).append(item)
        elif before_mark:
            if "." not in before_mark:
                prefix = get_filename(item)
                before_mark = prefix + "." + before_mark
            before.setdefault(before_mark, []).append(item)
        elif after_mark:
            if "." not in after_mark:
                prefix = get_filename(item)
                after_mark = prefix + "." + after_mark

            after.setdefault(after_mark, []).append(item)
        else:
            for ordinal, position in orders_map.items():
                if ordinal in mark.args:
                    if position < 0:
                        end.setdefault(position, []).append(item)
                    else:
                        start.setdefault(position, []).append(item)
                    break
        return True
    for mark_name, order in orders_map.items():
        mark = item.get_marker(mark_name)
        if mark:
            order = int(order)
            if order < 0:
                end.setdefault(order, []).append(item)
            else:
                start.setdefault(order, []).append(item)
            return True
    unordered.append(item)
    return False

def insert(items, sort):
    list_items = []
    if isinstance(items, tuple):
        list_items = items[1]
    else:
        list_items = items
    sort += list_items

def insert_before( name, items, sort):
    regex_name = re.escape(name) + r"(:?\.\w+)?$"
    for pos, item in enumerate(sort):
        prefix = get_filename(item)
        item_name =  prefix + "." + item.location[2]
        if re.match(regex_name, item_name):
            if pos == 0:
                sort[:] = items + sort
            else:
                sort[pos:1] = items
            return True
    return False

def insert_after(name, items, sort):
    regex_name = re.escape(name) + r"(:?\.\w+)?$"
    for pos, item in reversed(list(enumerate(sort))):
        prefix = get_filename(item)
        item_name =  prefix + "." + item.location[2]
        if re.match(regex_name, item_name):
            sort[pos+1:1] = items
            return True

    return False

def pytest_collection_modifyitems(session, config, items):
    before_item = {}
    after_item = {}
    start_item = {}
    end_item = {}
    unordered_list = []

    for item in items:
        mark_binning(item, item.keywords.keys(), start_item, end_item, before_item, after_item, unordered_list)

    start_item = sorted(start_item.items())
    end_item = sorted(end_item.items())

    sorted_list = []

    for entries in start_item:
        insert(entries, sorted_list)
    insert(unordered_list, sorted_list)
    for entries in end_item:
        insert(entries, sorted_list)

    still_left = 0
    length = len(before_item) + len(after_item)

    while( still_left != length):
        still_left = length
        remove_labels = []
        for label, before in before_item.items():
            if insert_before(label, before, sorted_list):
                remove_labels.append(label)
        for label in remove_labels:
            del before_item[label]

        remove_labels = []
        for label, after in after_item.items():
            if insert_after(label, after, sorted_list):
                remove_labels.append(label)
        for label in remove_labels:
            del after_item[label]

        length = len(before_item) + len(after_item)
    if length:
        sys.stdout.write("WARNING: can not execute test relative to others: ")
        for label, entry in before_item.items():
            sys.stdout.write( label + " ")
            sorted_list += entry
        for label, entry in after_item.items():
            sys.stdout.write( label + " ")
            sorted_list += entry
        sys.stdout.flush()
        print("enqueue them behind the others")
    
    items[:] = sorted_list

