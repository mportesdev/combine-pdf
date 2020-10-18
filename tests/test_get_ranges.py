import pytest

from combinepdf.utils import get_ranges


@pytest.mark.parametrize(
    'user_str, num_pages, expected',
    (
        pytest.param('1', 10, [(0, 1)]),
        pytest.param('93-100', 100, [(92, 100)]),
        pytest.param('2, 4-7, 9', 10, [(1, 2), (3, 7), (8, 9)]),
        pytest.param('5, 1, 10', 10, [(4, 5), (0, 1), (9, 10)]),
        pytest.param('1-5, 12-13', 20, [(0, 5), (11, 13)]),
        pytest.param('12, 48, 96-100', 100, [(11, 12), (47, 48), (95, 100)]),
        pytest.param('36-42, 1, 21-23, 50, 8-18', 50,
                     [(35, 42), (0, 1), (20, 23), (49, 50), (7, 18)]),
    )
)
def test_typical_input(user_str, num_pages, expected):
    assert get_ranges(user_str, num_pages) == expected


@pytest.mark.parametrize(
    'user_str, num_pages, expected',
    (
        pytest.param('2,4-7,9', 10, [(1, 2), (3, 7), (8, 9)]),
        pytest.param('5,1,10', 10, [(4, 5), (0, 1), (9, 10)]),
        pytest.param('1-5,12-13', 20, [(0, 5), (11, 13)]),
        pytest.param('12,48,96-100', 100, [(11, 12), (47, 48), (95, 100)]),
        pytest.param('36-42,1,21-23,50,8-18', 50,
                     [(35, 42), (0, 1), (20, 23), (49, 50), (7, 18)]),
    )
)
def test_comma_delimited_input(user_str, num_pages, expected):
    assert get_ranges(user_str, num_pages) == expected


@pytest.mark.parametrize(
    'user_str, num_pages, expected',
    (
        pytest.param('2 4-7 9', 10, [(1, 2), (3, 7), (8, 9)]),
        pytest.param('5 1 10', 10, [(4, 5), (0, 1), (9, 10)]),
        pytest.param('1-5 12-13', 20, [(0, 5), (11, 13)]),
        pytest.param('12 48 96-100', 100, [(11, 12), (47, 48), (95, 100)]),
        pytest.param('36-42 1 21-23 50 8-18', 50,
                     [(35, 42), (0, 1), (20, 23), (49, 50), (7, 18)]),
    )
)
def test_space_delimited_input(user_str, num_pages, expected):
    assert get_ranges(user_str, num_pages) == expected


@pytest.mark.parametrize(
    'user_str, num_pages',
    (
        pytest.param('', 100),
        pytest.param(' ', 100),
        pytest.param('  ', 100),
        pytest.param(',', 100),
        pytest.param(',,', 100),
        pytest.param(', ', 100),
        pytest.param(' ,', 100),
        pytest.param(' , , ,  ', 100),
        pytest.param(',, , ,', 100),
    )
)
def test_empty_input(user_str, num_pages):
    assert get_ranges(user_str, num_pages) == []


@pytest.mark.parametrize(
    'user_str, num_pages, expected',
    (
        pytest.param(',2', 100, [(1, 2)]),
        pytest.param(',,,,6', 100, [(5, 6)]),
        pytest.param(',9-10', 10, [(8, 10)]),
        pytest.param(',,,1-10', 10, [(0, 10)]),
    )
)
def test_input_with_leading_comma(user_str, num_pages, expected):
    assert get_ranges(user_str, num_pages) == expected


@pytest.mark.parametrize(
    'user_str, num_pages, expected',
    (
        pytest.param('2,', 100, [(1, 2)]),
        pytest.param('6,,,,', 100, [(5, 6)]),
        pytest.param('9-10,', 10, [(8, 10)]),
        pytest.param('1-10,,,', 10, [(0, 10)]),
    )
)
def test_input_with_trailing_comma(user_str, num_pages, expected):
    assert get_ranges(user_str, num_pages) == expected


@pytest.mark.parametrize(
    'user_str, num_pages, expected',
    (
        pytest.param('2-4 ,  ,12-40 ', 100, [(1, 4), (11, 40)]),
        pytest.param(',, , 6-8,  ,, 1 ,', 10, [(5, 8), (0, 1)]),
        pytest.param('  3-8 ,  12-100', 100, [(2, 8), (11, 100)]),
    )
)
def test_input_with_commas_and_whitespace(user_str, num_pages, expected):
    assert get_ranges(user_str, num_pages) == expected


@pytest.mark.parametrize(
    'user_str, num_pages, expected',
    (
        pytest.param('01', 100, [(0, 1)]),
        pytest.param('000008', 100, [(7, 8)]),
        pytest.param('01-05, 12-000013', 20, [(0, 5), (11, 13)]),
        pytest.param('12, 48, 0096-0100', 100, [(11, 12), (47, 48), (95, 100)]),
    )
)
def test_input_with_leading_zeros(user_str, num_pages, expected):
    assert get_ranges(user_str, num_pages) == expected


@pytest.mark.parametrize(
    'user_str, num_pages',
    (
        pytest.param('1', 0),
        pytest.param('0', 200),
        pytest.param(',,20,,,', 10),
    )
)
def test_value_out_of_range_raises_value_error(user_str, num_pages):
    with pytest.raises(ValueError, match=r'value [0-9]+ out of range'):
        get_ranges(user_str, num_pages)


@pytest.mark.parametrize(
    'user_str, num_pages',
    (
        pytest.param('1-5, 12, 48, 96-98', 97),
        pytest.param('  , 1-2  ,,', 1),
        pytest.param('7-11', 10),
        pytest.param('5-1', 10),
        pytest.param('97-1', 97),
    )
)
def test_interval_out_of_range_raises_value_error(user_str, num_pages):
    with pytest.raises(ValueError, match=r'interval [0-9\-]+ out of range'):
        get_ranges(user_str, num_pages)


@pytest.mark.parametrize(
    'user_str, num_pages',
    (
        pytest.param('3-', 100),
        pytest.param('0x21', 100),
        pytest.param('++55', 100),
        pytest.param('+1', 100, id='leading plus'),
        pytest.param('9, +1, 2', 10, id='leading plus'),
        pytest.param('+2-5', 100, id='leading plus'),
        pytest.param('1 - 2', 1, id='space around hyphen'),
        pytest.param('2-4,12 -40 ', 100, id='space around hyphen'),
        pytest.param('3-8,12- 100', 100, id='space around hyphen'),
    )
)
def test_invalid_input_raises_value_error(user_str, num_pages):
    with pytest.raises(ValueError, match=r'invalid input'):
        get_ranges(user_str, num_pages)


@pytest.mark.parametrize(
    'user_str, num_pages',
    (
        pytest.param('-1', 10),
        pytest.param('1,-8', 100),
        pytest.param('20 -55', 100),
        pytest.param(' -5 ', 10),
        pytest.param('3--3', 100),
        pytest.param('3 - -3', 100),
        pytest.param('-3-3', 100),
        pytest.param('-3 - 3', 100),
    )
)
def test_negative_value_is_invalid(user_str, num_pages):
    with pytest.raises(ValueError, match=r'invalid input'):
        get_ranges(user_str, num_pages)
