import pytest

from combinepdf.utils import trimmed_basename


@pytest.mark.parametrize(
    'filename, expected',
    (
        pytest.param(
            '/home/user/pdf/PDF_file.pdf',
            'PDF_file.pdf',
            id='12 no trim'
        ),
        pytest.param(
            '/home/user/pdf/'
            'PDF_2018-0010-0031-0014-0058-0000_This_is_a_nice_sample_PDF_'
            'file_which_has_a_really_long_name_0000001_0000002.pdf',
            'PDF_2018-0010-0031-0014-0058-0000_This_is_a_nice_sample_PDF_'
            'file_which_has_a_...',
            id='113 trim to 80'
        ),
    )
)
def test_with_default_max_length(filename, expected):
    result = trimmed_basename(filename)
    assert result == expected


@pytest.mark.parametrize(
    'filename, max_length, expected',
    (
        pytest.param(
            '/home/user/pdf/a_PDF_file.pdf',
            20,
            'a_PDF_file.pdf',
            id='14 no trim'
        ),
        pytest.param(
            '/home/user/pdf/a_PDF_file.pdf',
            10,
            'a_PDF_f...',
            id='14 trim to 10'
        ),
        pytest.param(
            '/home/user/pdf/'
            'This_is_a_sample_file_with_a_not_so_long_name.pdf',
            62,
            'This_is_a_sample_file_with_a_not_so_long_name.pdf',
            id='49 no trim'
        ),
        pytest.param(
            '/home/user/pdf/'
            'PDF_2018-0010-0031-0014-0058-0000_This_is_a_nice_sample_PDF_'
            'file_which_has_a_really_long_name_0000001_0000002.pdf',
            100,
            'PDF_2018-0010-0031-0014-0058-0000_This_is_a_nice_sample_PDF_'
            'file_which_has_a_really_long_name_000...',
            id='113 trim to 100'
        ),
        pytest.param(
            '/home/user/pdf/'
            'PDF_2018-0010-0031-0014-0058-0000_This_is_a_sample_PDF_file_'
            'which_has_a_really_long_name_0000001_0000002.pdf',
            42,
            'PDF_2018-0010-0031-0014-0058-0000_This_...',
            id='108 trim to 42'
        ),
        pytest.param(
            '/home/user/pdf/'
            'PDF_2018-0010-0031-0014-0058-0000_This_is_a_nice_sample_PDF_'
            'file_which_has_a_really_long_name_0000001.pdf',
            120,
            'PDF_2018-0010-0031-0014-0058-0000_This_is_a_nice_sample_PDF_'
            'file_which_has_a_really_long_name_0000001.pdf',
            id='105 no trim'
        ),
    )
)
def test_with_set_max_length(max_length, filename, expected):
    result = trimmed_basename(filename, max_length=max_length)
    assert result == expected
