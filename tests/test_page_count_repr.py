import pytest

from combinepdf.utils import page_count_repr


@pytest.mark.parametrize(
    'number, expected',
    (
        pytest.param(0, '0 pages'),
        pytest.param(1, '1 page'),
        pytest.param(2, '2 pages'),
        pytest.param(42, '42 pages'),
    )
)
def test_typical_input(number, expected):
    assert page_count_repr(number) == expected
