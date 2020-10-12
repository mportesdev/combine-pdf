import pytest

from combinepdf.utils import get_ranges


def test_typical_input():
    user_str = '1-5, 12, 48, 96-98'
    num_pages = 98
    expected = [(0, 5), (11, 12), (47, 48), (95, 98)]
    assert get_ranges(user_str, num_pages) == expected


@pytest.mark.parametrize(
    'user_str, num_pages',
    (
        pytest.param('', 100),
        pytest.param(' ', 100),
        pytest.param('          ', 100),
    )
)
def test_empty_input(user_str, num_pages):
    assert get_ranges(user_str, num_pages) == []


@pytest.mark.parametrize(
    'user_str, num_pages, expected',
    (
        pytest.param(',2', 100, [(1, 2)]),
        pytest.param(',,,,6', 100, [(5, 6)]),
        pytest.param(',,9-10', 10, [(8, 10)]),
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
        pytest.param('9-10,,', 10, [(8, 10)]),
        pytest.param('1-10,,,', 10, [(0, 10)]),
    )
)
def test_input_with_trailing_comma(user_str, num_pages, expected):
    assert get_ranges(user_str, num_pages) == expected


@pytest.mark.parametrize(
    'user_str, num_pages, expected',
    (
        pytest.param('2-4 ,  ,12  -40 ', 100, [(1, 4), (11, 40)]),
        pytest.param(',, , 6-8,  ,, 1 ,', 10, [(5, 8), (0, 1)]),
        pytest.param('  3  -   8 ,  12-  100', 100, [(2, 8), (11, 100)]),
    )
)
def test_input_with_commas_and_whitespace(user_str, num_pages, expected):
    assert get_ranges(user_str, num_pages) == expected


@pytest.mark.parametrize(
    'user_str, num_pages',
    (
        pytest.param('1', 0),
        pytest.param('0', 200),
        pytest.param(',,20,,,', 10),
        pytest.param('1-5, 12, 48, 96-98', 97),
        pytest.param('  , 1  -  2  ,,', 1),
        pytest.param('5-1', 10),
        pytest.param('7-11', 10),
    )
)
def test_input_out_of_range_raises_value_error(user_str, num_pages):
    with pytest.raises(ValueError):
        get_ranges(user_str, num_pages)


@pytest.mark.parametrize(
    'user_str, num_pages',
    (
        pytest.param('3-', 100),
        pytest.param('-8', 100),
        pytest.param('0x21', 100),
        pytest.param('++55', 100),
    )
)
def test_invalid_input_raises_value_error(user_str, num_pages):
    with pytest.raises(ValueError):
        get_ranges(user_str, num_pages)
