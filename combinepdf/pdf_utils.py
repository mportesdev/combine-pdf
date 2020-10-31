import pictureshow
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import A4

save_image_as_pdf = pictureshow.picture_to_pdf


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
