import json
import os
from types import SimpleNamespace

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.utils import PdfReadError
from PySide2 import QtWidgets, QtGui, QtCore

from . import etc, utils


class FileBox(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setAutoFillBackground(True)
        self.default_bg = self.palette().color(self.palette().Window)

        self.filename = ''
        # number of pages of the currently open PDF file
        self.pages = 0
        # list of tuples representing page ranges selected for output
        self.output_tuples = []
        self.output_page_count = 0

        # first row of widgets
        self.button_Browse = QtWidgets.QPushButton('Select PDF...')
        self.button_Browse.clicked.connect(self.open_file)

        self.button_Image = QtWidgets.QPushButton('Select image...')
        self.button_Image.clicked.connect(self.open_image_file)

        self.button_Blank = QtWidgets.QPushButton('Blank page')
        self.button_Blank.clicked.connect(self.add_blank_page)

        # TODO: wrap long filenames so that the window width doesn't change
        self.filename_label = QtWidgets.QLabel()
        self.filename_label.setVisible(False)

        self.pages_info = QtWidgets.QLabel()
        self.pages_info.setStyleSheet(etc.INFO_LABEL)

        self.button_Remove = QtWidgets.QPushButton()
        self.button_Remove.setIcon(QtGui.QIcon(etc.ICON_TRASH))
        self.button_Remove.setToolTip('Remove this file')
        self.button_Remove.setFixedWidth(30)
        self.button_Remove.clicked.connect(self.remove_file)
        self.button_Remove.setVisible(False)

        # second row of widgets
        self.rbutton_All = QtWidgets.QRadioButton('All')
        self.rbutton_All.toggled.connect(self.switch_rbuttons)
        self.rbutton_All.setVisible(False)

        self.rbutton_Pages = QtWidgets.QRadioButton('Pages')
        self.rbutton_Pages.setVisible(False)

        self.rbutton_group = QtWidgets.QButtonGroup()
        self.rbutton_group.addButton(self.rbutton_All)
        self.rbutton_group.addButton(self.rbutton_Pages)

        self.page_select_edit = QtWidgets.QLineEdit()
        self.page_select_edit.setPlaceholderText('Example: 1, 3-5, 8')
        self.page_select_edit.textEdited.connect(self.update_select_info)
        self.page_select_edit.textEdited.connect(self.parent()
                                                 .update_main_button)
        self.page_select_edit.setVisible(False)

        self.page_select_info = QtWidgets.QLabel()
        self.page_select_info.setVisible(False)
        self.page_select_info.setStyleSheet(etc.INFO_LABEL)

        self.spacer = QtWidgets.QSpacerItem(30, 0)

        # layout
        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.button_Browse, 1, 0)
        self.layout.addWidget(self.button_Image, 1, 1)
        self.layout.addWidget(self.button_Blank, 1, 2)
        self.layout.addWidget(self.filename_label, 1, 2, 1, 3)
        self.layout.addWidget(self.pages_info, 1, 5)
        self.layout.addWidget(self.button_Remove, 1, 6)
        self.layout.addWidget(self.rbutton_All, 2, 2)
        self.layout.addWidget(self.rbutton_Pages, 2, 3)
        self.layout.addWidget(self.page_select_edit, 2, 4)
        self.layout.addWidget(self.page_select_info, 2, 5)
        self.layout.addItem(self.spacer, 2, 6)

        for column, stretch in zip((2, 3, 4, 5), (10, 10, 55, 25)):
            self.layout.setColumnStretch(column, stretch)
        self.setLayout(self.layout)

    def add_blank_page(self):
        set_widget_background(self, 0xffffffff)
        self.filename_label.setText('BLANK PAGE')
        self.filename_label.setToolTip('')
        self.filename_label.setVisible(True)
        self.button_Browse.setVisible(False)
        self.button_Image.setVisible(False)
        self.button_Blank.setVisible(False)
        self.button_Remove.setVisible(True)
        self.pages = 1
        self.output_page_count = 1
        self.parent().update_main_button()

    def open_file(self):
        filename, __ = QtWidgets.QFileDialog.getOpenFileName(
            self.parent(),
            'Open a PDF file',
            self.parent().config.open_path,
            'PDF files (*.pdf)',
        )

        if not filename:
            return

        self.parent().config.open_path = os.path.split(filename)[0]
        try:
            reader = PdfFileReader(filename)
            num_pages = reader.numPages
        except PdfReadError as err:
            MainWindow.message_box(icon=QtWidgets.QMessageBox.Warning,
                                   title='Warning',
                                   text='File could not be read.',
                                   detailed=f'File: {filename}\n\n'
                                            f'Error: {err!r}')
        else:
            set_widget_background(self, 0xffd8e8ff)
            if self.filename == '':
                self.button_Browse.setVisible(False)
                self.button_Image.setVisible(False)
                self.button_Blank.setVisible(False)
                self.filename_label.setVisible(True)
                self.button_Remove.setVisible(True)
                self.rbutton_All.setVisible(True)
                self.rbutton_Pages.setVisible(True)
                self.page_select_edit.setVisible(True)
            self.filename = filename
            self.pages = num_pages
            self.update_output([(0, num_pages)])
            self.filename_label.setText(os.path.basename(filename))
            self.filename_label.setToolTip(filename)
            self.rbutton_All.setChecked(True)
            self.pages_info.setText(f'{utils.page_count_repr(num_pages)} total')
            self.parent().update_main_button()
            self.page_select_edit.setText('')

    def open_image_file(self):
        filename, __ = QtWidgets.QFileDialog.getOpenFileName(
            self.parent(),
            'Open an image file',
            self.parent().config.image_path,
            'Image files (*.png; *.jpg; *.jpeg; *.gif; *.bmp)'
        )

        if not filename:
            return

        self.parent().config.image_path = os.path.split(filename)[0]
        temp_pdf_filename = filename + '.CPDF_TEMP.pdf'
        try:
            utils.save_image_as_pdf(filename, temp_pdf_filename)
        # PIL.UnidentifiedImageError is subclass of OSError
        except OSError as err:
            MainWindow.message_box(icon=QtWidgets.QMessageBox.Warning,
                                   title='Warning',
                                   text='Image to PDF conversion failed.',
                                   detailed=f'File: {filename}\n\n'
                                            f'Error: {err!r}')
        else:
            set_widget_background(self, 0xffd0f0d0)
            if self.filename == '':
                self.button_Browse.setVisible(False)
                self.button_Image.setVisible(False)
                self.button_Blank.setVisible(False)
                self.filename_label.setVisible(True)
                self.button_Remove.setVisible(True)
            self.filename = temp_pdf_filename
            self.pages = 1
            self.update_output([(0, 1)])
            self.filename_label.setText(os.path.basename(filename))
            self.filename_label.setToolTip(filename)
            self.parent().update_main_button()

    def remove_file(self):
        set_widget_background(self, self.default_bg)
        self.filename = ''
        self.pages = 0
        self.update_output([])
        self.button_Browse.setVisible(True)
        self.button_Image.setVisible(True)
        self.button_Blank.setVisible(True)
        self.filename_label.setVisible(False)
        self.pages_info.setText('')
        self.button_Remove.setVisible(False)
        self.rbutton_All.setVisible(False)
        self.rbutton_Pages.setVisible(False)
        self.page_select_edit.setVisible(False)
        self.page_select_info.setVisible(False)
        self.parent().update_main_button()

    def switch_rbuttons(self):
        if self.rbutton_All.isChecked():
            self.update_output([(0, self.pages)])
            self.page_select_edit.setEnabled(False)
            self.page_select_info.setVisible(False)
        else:
            self.update_select_info()
            self.page_select_edit.setEnabled(True)
            self.page_select_edit.setFocus()
            self.page_select_info.setVisible(True)
        self.parent().update_main_button()

    def update_output(self, tuples):
        self.output_tuples = tuples
        self.output_page_count = sum(len(range(*tup)) for tup in tuples)

    def update_select_info(self):
        text = self.page_select_edit.text()
        self.update_output(utils.string_to_range_tuples(text, self.pages))

        if self.output_tuples or text == '':
            self.page_select_edit.setStyleSheet('')
            self.page_select_info.setText(
                f'{utils.page_count_repr(self.output_page_count)} selected')
        else:
            self.page_select_info.setText('')
            self.page_select_edit.setStyleSheet(etc.INVALID)


def set_widget_background(widget, color):
    palette = widget.palette()
    palette.setColor(palette.Window, QtGui.QColor(color))
    widget.setPalette(palette)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CombinePDF')
        self.resize(QtCore.QSize(640, 300))

        config_dict = dict(open_path=os.curdir, image_path=os.curdir,
                           save_path=os.curdir,
                           save_filename='Combined.pdf', num_items=3)
        try:
            with open('config.json') as f:
                config_dict.update(json.load(f))
        # json.decoder.JSONDecodeError is subclass of ValueError
        except (FileNotFoundError, ValueError):
            pass

        self.config = SimpleNamespace(**config_dict)

        # list of FileBox objects; can be appended by 'add_item' method
        self.file_boxes = [FileBox(self)
                           for __ in range(self.config.num_items)]

        button_Help = QtWidgets.QPushButton('Help')
        button_Help.setIcon(QtGui.QIcon(etc.ICON_QUESTION))
        button_Help.clicked.connect(self.help_box)

        button_About = QtWidgets.QPushButton('About')
        button_About.setIcon(QtGui.QIcon(etc.ICON_INFO))
        button_About.clicked.connect(self.about_box)

        top_layout = QtWidgets.QGridLayout()
        top_layout.addWidget(button_Help, 0, 1)
        top_layout.addWidget(button_About, 0, 2)

        for column, stretch in zip((0, 1, 2), (10, 1, 1)):
            top_layout.setColumnStretch(column, stretch)

        self.central_layout = QtWidgets.QVBoxLayout()

        for file_box in self.file_boxes:
            self.central_layout.addWidget(file_box)

        button_Add = QtWidgets.QPushButton('&Add')
        button_Add.setIcon(QtGui.QIcon(etc.ICON_PLUS))
        button_Add.setToolTip('Add another row (Alt+A)')
        button_Add.clicked.connect(self.add_item)

        self.button_Combine = QtWidgets.QPushButton('Combine && &Save')
        self.button_Combine.setIcon(QtGui.QIcon(etc.ICON_COMBINE))
        self.button_Combine.setFixedHeight(50)
        self.button_Combine.setToolTip('Save the combined PDF file (Alt+S)')
        self.button_Combine.clicked.connect(self.save_file)
        self.button_Combine.setEnabled(False)

        button_Exit = QtWidgets.QPushButton('E&xit')
        button_Exit.setIcon(QtGui.QIcon(etc.ICON_EXIT))
        button_Exit.setFixedHeight(50)
        button_Exit.setToolTip('Exit the application (Alt+X)')
        button_Exit.clicked.connect(self.exit)

        bottom_layout = QtWidgets.QGridLayout()
        bottom_layout.addWidget(button_Add, 0, 0)
        bottom_layout.addWidget(self.button_Combine, 1, 2)
        bottom_layout.addWidget(button_Exit, 1, 3)

        for column, stretch in zip((0, 1, 2, 3, 4), (1, 1, 3, 1, 2)):
            bottom_layout.setColumnStretch(column, stretch)

        master_layout = QtWidgets.QVBoxLayout()
        master_layout.addLayout(top_layout)
        master_layout.addLayout(self.central_layout)
        master_layout.addLayout(bottom_layout)
        self.setLayout(master_layout)

    def save_file(self):
        output_filename, __ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            'Save PDF file as...',
            os.path.join(self.config.save_path, self.config.save_filename),
            'PDF files (*.pdf)',
        )

        if not output_filename:
            return

        self.config.save_path, self.config.save_filename = os.path.split(output_filename)
        if output_filename in (f_box.filename for f_box in self.file_boxes):
            self.message_box(icon=QtWidgets.QMessageBox.Warning,
                             title='Warning',
                             text='You are not allowed to overwrite '
                                  'one of the input files.',
                             informative='Please select a different '
                                         'filename.')
            # TODO: dialog
            #  'Do you really wish to overwrite one of the input files?'
        else:
            # TODO: handle PyPDF2's custom exceptions during the
            #  merge process
            writer = PdfFileWriter()
            for file_box in self.file_boxes:
                filename = file_box.filename
                if filename:
                    reader = PdfFileReader(filename)
                    # add pages according to "range tuples"
                    for start, stop in file_box.output_tuples:
                        for page in reader.pages[start:stop]:
                            writer.addPage(page)
                elif file_box.pages:
                    # file_box with a blank page is recognized by
                    # (file_box.filename == '' and file_box.pages != 0)
                    writer.addBlankPage(*utils.page_A4_dimensions())

            with open(output_filename, 'wb') as f:
                writer.write(f)

    def update_main_button(self):
        total_pages = sum(f_box.output_page_count for f_box in self.file_boxes)
        if total_pages > 0:
            self.button_Combine.setText(
                f'Combine && &Save {utils.page_count_repr(total_pages)}')
            self.button_Combine.setEnabled(True)
        else:
            self.button_Combine.setText('Combine && &Save')
            self.button_Combine.setEnabled(False)

    def add_item(self):
        file_box = FileBox(self)
        self.file_boxes.append(file_box)
        self.central_layout.addWidget(file_box)

    def help_box(self):
        self.message_box(icon=QtWidgets.QMessageBox.Information,
                         title='Help', text=etc.HELP_TEXT)

    def about_box(self):
        self.message_box(icon=QtWidgets.QMessageBox.Information,
                         title='About', text=etc.ABOUT_TEXT)

    def run(self, app):
        self.show()
        app.exec_()

    def exit(self):
        with open('config.json', 'w') as file:
            json.dump(self.config.__dict__, file, indent=4)
        self.close()

    @staticmethod
    def message_box(icon, title, text, detailed=None, informative=None):
        message = QtWidgets.QMessageBox(icon, title, text)
        if detailed:
            message.setDetailedText(detailed)
        if informative:
            message.setInformativeText(informative)
        message.exec_()


def main():
    app = QtWidgets.QApplication()
    app_window = MainWindow()
    app_window.run(app)


if __name__ == '__main__':
    main()
