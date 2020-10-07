import os
import random
import string

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from . import constants


def string_to_range_tuples(user_string: str, number_of_pages: int) -> list:
    """Return a list of tuples if user_string is valid, an empty list
    otherwise. From the user's point of view, pages are numbered from 1.
    In PdfFileMerger's interface, pages are numbered from 0.

    Example: string_to_range_tuples('1-5, 12, 48, 96-98', 98)
    return value: [(0, 5), (11, 12), (47, 48), (95, 98)]
    """
    # TODO: rewrite using regexps
    result = []
    valid = True

    if user_string:
        user_string = user_string.strip(' ,')
        for part in user_string.split(','):

            if part.strip() == '':
                continue

            try:
                # valid single number?
                from_page = int(part.strip())
            except ValueError:
                # not a single number

                try:
                    # valid range of numbers?
                    from_page = int(part.split('-')[0].strip())
                    to_page = int(part.split('-', 1)[1].strip())
                except ValueError:
                    # not a valid range of numbers
                    valid = False
                    break
                else:
                    # valid range of numbers

                    if 1 <= from_page <= to_page <= number_of_pages:
                        # valid page range -> make a tuple to be directly
                        # passed to merger.append() (pages numbered from 0)
                        range_tuple = (from_page - 1, to_page)
                    else:
                        # range of numbers out of page range
                        valid = False
                        break
            else:
                # some single number

                if 1 <= from_page <= number_of_pages:
                    # valid page number -> make a tuple to be directly
                    # passed to merger.append() (pages numbered from 0)
                    range_tuple = (from_page - 1, from_page)
                else:
                    # number out of page range
                    valid = False
                    break
            result.append(range_tuple)

    return result if valid else []


def page_count_repr(count):
    word = 'page' if count == 1 else 'pages'
    return f'{count} {word}'


def page_A4_dimensions(mode='portrait', dpi=72):
    page_A4_milimeters = (210, 297) if mode == 'portrait' else (297, 210)
    return tuple(dimension / 25.4 * dpi for dimension in page_A4_milimeters)


def get_temporary_filename(suffix):
    filename = ''.join(random.choices(string.ascii_letters, k=50)) + suffix
    return os.path.join(constants.TEMP_DIR, filename)


def save_image_as_pdf(img_file, pdf_file, page_size=A4, margin=0,
                      stretch_small=False):
    page_width, page_height = page_size
    area_width, area_height = page_width - 2*margin, page_height - 2*margin

    img = ImageReader(img_file)
    img_width, img_height = img.getSize()
    image_is_big = img_width > area_width or img_height > area_height
    image_is_wide = img_width / img_height > area_width / area_height

    # calculate scale factor to fit image to area
    if image_is_big or stretch_small:
        scale = (area_width / img_width if image_is_wide
                 else area_height / img_height)
    else:
        scale = 1

    # center scaled image to area
    x = margin + (area_width - img_width * scale) / 2
    y = margin + (area_height - img_height * scale) / 2

    pdf_canvas = Canvas(pdf_file, pagesize=page_size)
    pdf_canvas.drawImage(
        img, x, y, width=img_width * scale, height=img_height * scale
    )
    pdf_canvas.save()
