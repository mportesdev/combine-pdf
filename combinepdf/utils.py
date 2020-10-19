import os
import random
import re
import string

from . import constants


def get_ranges(user_string: str, number_of_pages: int) -> list:
    """Convert a string into a sequence of ranges.

    If `user_string` is valid, return a list of 2-tuples representing
    page ranges. Return an empty list if `user_string` is empty or
    contains only delimiters. Otherwise, raise ValueError.

    From the user's point of view, pages are numbered from 1.
    In PdfFileReader's interface, pages are numbered from 0.
    """
    result = []

    for part in re.split(r'[ ,]+', user_string):
        if part == '':
            continue

        match = re.match(r'^(\d+)(-(\d+))?$', part)
        if match is None:
            raise ValueError('invalid input')

        from_page = int(match[1])
        if match[3] is None:
            if 1 <= from_page <= number_of_pages:
                # valid page number
                result.append((from_page - 1, from_page))
            else:
                raise ValueError(f'value {from_page} out of range')
        else:
            to_page = int(match[3])
            if 1 <= from_page <= to_page <= number_of_pages:
                # valid page range
                result.append((from_page - 1, to_page))
            else:
                raise ValueError(f'interval {from_page}-{to_page} out of range')

    return result


def page_count_repr(number):
    noun = 'page' if number == 1 else 'pages'
    return f'{number} {noun}'


def get_temporary_filename(suffix):
    filename = ''.join(random.choices(string.ascii_letters, k=50)) + suffix
    return os.path.join(constants.TEMP_DIR, filename)
