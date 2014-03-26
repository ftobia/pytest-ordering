import re

from ._version import __version__


replacements = {
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
    """Register the "run" marker.
    """
    config_line = (
        'run: specify ordering information for when tests should run '
        'in relation to one another. Provided by pytest-ordering. '
        'See also: http://pytest-ordering.readthedocs.org/'
    )
    config.addinivalue_line('markers', config_line)


def pytest_collection_modifyitems(session, config, items):
    items[:] = list(_order_tests(items))


def orderable(marker_name, marker_info):
    if not hasattr(marker_info, 'kwargs'):
        return False
    if 'order' in marker_info.kwargs:
        return True
    match = re.match('^order(\d+)$', marker_name)
    return bool(match) or marker_name in replacements


def get_index(marker_name, marker_info):
    match = re.match('^order(\d+)$', marker_name)
    if match:
        return int(match.group(1)) - 1
    if marker_name in replacements:
        return replacements[marker_name]
    return marker_info.kwargs['order']


def split(dictionary):
    from_beginning, from_end = {}, {}
    for key, val in dictionary.items():
        if key >= 0:
            from_beginning[key] = val
        else:
            from_end[key] = val
    return from_beginning, from_end


def _order_tests(tests):
    ordered_tests = {}
    remaining_tests = []
    for test in tests:
        # There has got to be an API for this. :-/
        markers = test.keywords.__dict__['_markers']
        orderable_markers = [(k, v) for (k, v) in markers.items()
                             if orderable(k, v)]
        if len(orderable_markers) == 1:
            marker_name, marker_info = orderable_markers[0]
            ordered_tests[get_index(marker_name, marker_info)] = test
        else:
            remaining_tests.append(test)
    from_beginning, from_end = split(ordered_tests)
    remaining_iter = iter(remaining_tests)
    for i in range(max(from_beginning or [-1]) + 1):
        if i in from_beginning:
            yield from_beginning[i]
        else:
            yield next(remaining_iter)
    # TODO TODO TODO
    for i in range(min(from_end or [0]), 0):
        if i in from_end:
            yield from_end[i]
        else:
            yield next(remaining_iter)
    for test in remaining_iter:
        yield test
