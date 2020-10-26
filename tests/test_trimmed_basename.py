import pytest

from combinepdf.utils import trimmed_basename


@pytest.mark.parametrize(
    'filename, expected, expected_length',
    (
        pytest.param(
            '/home/user/pdf/PDF_file.pdf',
            'PDF_file.pdf',
            12,
            id='12 no trim'
        ),
        pytest.param(
            '/home/user/pdf/PDF_2018-0010-0031-0014-0058-0000_This_is_a_nice'
            '_sample_PDF_file_which_has_a_really_long_name_0000001_0000002.pdf',
            'PDF_2018-0010-0031-0014-0058-0000_This_is_a_nice'
            '_sample_PDF_file_which_has_a_...',
            80,
            id='113 trim to 80'
        ),
    )
)
def test_with_default_max_length(filename, expected, expected_length):
    result = trimmed_basename(filename)
    assert result == expected
    assert len(result) == expected_length


@pytest.mark.parametrize(
    'filename, max_length, expected, expected_length',
    (
        pytest.param(
            '/home/user/pdf/a_PDF_file.pdf',
            20, 'a_PDF_file.pdf',
            14,
            id='14 no trim'
        ),
        pytest.param(
            '/home/user/pdf/a_PDF_file.pdf',
            10,
            'a_PDF_f...', 10,
            id='14 trim to 10'
        ),
        pytest.param(
            '/home/user/pdf/This_is_a_sample_file_with_a_not_so_long_name.pdf',
            62,
            'This_is_a_sample_file_with_a_not_so_long_name.pdf',
            49,
            id='49 no trim'
        ),
        pytest.param(
            '/home/user/pdf/PDF_2018-0010-0031-0014-0058-0000_This_is_a_nice'
            '_sample_PDF_file_which_has_a_really_long_name_0000001_0000002.pdf',
            100,
            'PDF_2018-0010-0031-0014-0058-0000_This_is_a_nice'
            '_sample_PDF_file_which_has_a_really_long_name_000...',
            100,
            id='113 trim to 100'
        ),
        pytest.param(
            '/home/user/pdf/PDF_2018-0010-0031-0014-0058-0000_This_is_a'
            '_sample_PDF_file_which_has_a_really_long_name_0000001_0000002.pdf',
            42,
            'PDF_2018-0010-0031-0014-0058-0000_This_...',
            42,
            id='108 trim to 42'
        ),
        pytest.param(
            '/home/user/pdf/PDF_2018-0010-0031-0014-0058-0000_This_is_a_nice'
            '_sample_PDF_file_which_has_a_really_long_name_0000001.pdf',
            120,
            'PDF_2018-0010-0031-0014-0058-0000_This_is_a_nice'
            '_sample_PDF_file_which_has_a_really_long_name_0000001.pdf',
            105,
            id='105 no trim'
        ),
    )
)
def test_with_set_max_length(max_length, filename, expected, expected_length):
    result = trimmed_basename(filename, max_length=max_length)
    assert result == expected
    assert len(result) == expected_length
