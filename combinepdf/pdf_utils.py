from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas


def get_pdf_num_pages(filename):
    reader = PdfFileReader(filename)
    return reader.numPages


def write_combined_pdf(input_items, output_file):
    writer = PdfFileWriter()

    for item in input_items:
        if item.filename:
            reader = PdfFileReader(item.filename)
            for start, stop in item.output_tuples:
                for page in reader.pages[start:stop]:
                    writer.addPage(page)
        elif item.pages:
            # a blank page is recognized by empty `filename`
            # and non-zero `pages`
            writer.addBlankPage(*A4)

    with open(output_file, 'wb') as f:
        writer.write(f)


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
