#!/usr/bin/python
# coding: utf-8

import os
import json
import PyPDF2
from PySide2 import QtWidgets, QtGui, QtCore
import utils


class FileBox:
    def __init__(self, parent_app, filename, pages, output_tuples):
        self.parent_app = parent_app
        self.filename = filename
        # number of pages of the currently open PDF file
        self.pages = pages
        # list of tuples representing page ranges selected for output
        self.update_output(output_tuples)

        # first row of widgets
        self.button_Browse = QtWidgets.QPushButton("Select file...")
        self.button_Browse.clicked.connect(self.open_file)

        self.filename_label = QtWidgets.QLabel("[no file]")
        self.filename_label.setEnabled(False)

        self.pages_info = QtWidgets.QLabel()
        self.pages_info.setStyleSheet("color: #477b6e")

        self.button_Remove = QtWidgets.QPushButton()
        self.button_Remove.setIcon(QtGui.QIcon("icons/trash.png"))
        self.button_Remove.setToolTip("Remove this file")
        self.button_Remove.setFixedWidth(30)
        self.button_Remove.clicked.connect(self.remove_file)
        self.button_Remove.clicked.connect(self.parent_app.update_main_button)
        self.button_Remove.setVisible(False)

        # second row of widgets
        self.rbutton_All = QtWidgets.QRadioButton("All")
        self.rbutton_All.toggled.connect(self.switch_rbuttons)
        self.rbutton_All.toggled.connect(self.parent_app.update_main_button)
        self.rbutton_All.setVisible(False)

        self.rbutton_Pages = QtWidgets.QRadioButton("Pages")
        self.rbutton_Pages.setVisible(False)

        self.rbutton_group = QtWidgets.QButtonGroup()
        self.rbutton_group.addButton(self.rbutton_All)
        self.rbutton_group.addButton(self.rbutton_Pages)

        self.page_select_edit = QtWidgets.QLineEdit()
        self.page_select_edit.setPlaceholderText("Example: 1, 3-5, 8")
        self.page_select_edit.textEdited.connect(self.update_select_info)
        self.page_select_edit.textEdited.connect(self.parent_app
                                                 .update_main_button)
        self.page_select_edit.setVisible(False)

        self.page_select_info = QtWidgets.QLabel()
        self.page_select_info.setVisible(False)
        self.page_select_info.setStyleSheet("color: #477b6e")

        self.spacer = QtWidgets.QSpacerItem(30, 0)

        # only for column width testing:
        # self.filename_label.setStyleSheet("background: #ddd")
        # self.pages_info.setStyleSheet("background: #ddd")
        # self.pages_info.setStyleSheet("background: #ddd")
        # self.rbutton_All.setStyleSheet("background: #ddd")
        # self.rbutton_Pages.setStyleSheet("background: #ddd")
        # self.page_select_info.setStyleSheet("background: #ddd")

        # layout
        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.button_Browse, 1, 0)
        self.layout.addWidget(self.filename_label, 1, 1, 1, 3)
        self.layout.addWidget(self.pages_info, 1, 4)
        self.layout.addWidget(self.button_Remove, 1, 5)
        self.layout.addWidget(self.rbutton_All, 2, 1)
        self.layout.addWidget(self.rbutton_Pages, 2, 2)
        self.layout.addWidget(self.page_select_edit, 2, 3)
        self.layout.addWidget(self.page_select_info, 2, 4)
        self.layout.addItem(self.spacer, 2, 5)

        for column, stretch in zip((1, 2, 3, 4), (10, 10, 55, 25)):
            self.layout.setColumnStretch(column, stretch)

    def open_file(self):
        filename, __ = QtWidgets.QFileDialog.getOpenFileName(
                       self.parent_app, "Open a PDF file",
                       self.parent_app.config.get("open path", os.curdir),
                       "PDF files (*.pdf)")

        if filename:
            self.parent_app.config["open path"] = os.path.split(filename)[0]
            try:
                reader = PyPDF2.PdfFileReader(filename)
                num_pages = reader.numPages
            except Exception as err:
                MainWindow.message_box(icon=QtWidgets.QMessageBox.Warning,
                                       title="Warning",
                                       text="File could not be read.",
                                       detailed="File: {}\n\nError: {}"
                                                .format(filename, err))
            else:
                if self.filename == "":
                    self.filename_label.setEnabled(True)
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
                self.pages_info.setText("{} {} total".format(num_pages,
                                        "pages" if num_pages > 1 else "page"))
                self.page_select_edit.setText("")

    def remove_file(self):
        self.filename = ""
        self.pages = 0
        self.update_output([])
        self.filename_label.setText("[no file]")
        self.filename_label.setEnabled(False)
        self.filename_label.setToolTip("")
        self.pages_info.setText("")
        self.button_Remove.setVisible(False)
        self.rbutton_All.setVisible(False)
        self.rbutton_Pages.setVisible(False)
        self.page_select_edit.setVisible(False)
        self.page_select_info.setVisible(False)

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

    def update_output(self, tuples):
        self.output_tuples = tuples
        self.output_page_count = sum(len(range(*tup)) for tup in tuples)

    def update_select_info(self):
        self.update_output(utils.string_to_range_tuples(
                                     self.page_select_edit.text(), self.pages))
        if self.output_tuples:
            self.page_select_info.setText("{} {} selected"
                                          .format(self.output_page_count,
                                                  "pages"
                                                  if self.output_page_count > 1
                                                  else "page"))
        else:
            self.page_select_info.setText("selection not valid")


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CombinePDF")
        self.resize(QtCore.QSize(640, 300))

        try:
            with open("config.json") as f:
                self.config = json.load(f)
        # json.decoder.JSONDecodeError is subclass of ValueError
        except (FileNotFoundError, ValueError):
            self.config = {"open path": os.curdir,
                           "save path": os.curdir,
                           "save filename": "joined-pdf.pdf",
                           "# of items": 3}

        # list of FileBox objects; can be appended by 'add_item' method
        self.file_boxes = [FileBox(parent_app=self, filename="",
                                   pages=0, output_tuples=[])
                           for __ in range(self.config.get("# of items", 3))]

        button_Help = QtWidgets.QPushButton("Help")
        button_Help.setIcon(QtGui.QIcon("icons/question.png"))
        button_Help.clicked.connect(self.help_box)

        button_About = QtWidgets.QPushButton("About")
        button_About.setIcon(QtGui.QIcon("icons/info.png"))
        button_About.clicked.connect(self.about_box)

        top_layout = QtWidgets.QGridLayout()
        top_layout.addWidget(button_Help, 0, 1)
        top_layout.addWidget(button_About, 0, 2)

        for column, stretch in zip((0, 1, 2), (10, 1, 1)):
            top_layout.setColumnStretch(column, stretch)

        self.central_layout = QtWidgets.QVBoxLayout()

        line = QtWidgets.QLabel()
        line.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Sunken)
        self.central_layout.addWidget(line)

        for file_box in self.file_boxes:
            self.central_layout.addLayout(file_box.layout)
            line = QtWidgets.QLabel()
            line.setFrameStyle(QtWidgets.QFrame.HLine
                               | QtWidgets.QFrame.Sunken)
            self.central_layout.addWidget(line)

        button_Add = QtWidgets.QPushButton("&Add")
        button_Add.setIcon(QtGui.QIcon("icons/plus.png"))
        button_Add.setToolTip("Add another row (Alt+A)")
        button_Add.clicked.connect(self.add_item)

        self.button_Combine = QtWidgets.QPushButton("Combine && &Save")
        self.button_Combine.setIcon(QtGui.QIcon("icons/combine.png"))
        self.button_Combine.setFixedHeight(50)
        self.button_Combine.setToolTip("Save the combined PDF file (Alt+S)")
        self.button_Combine.clicked.connect(self.save_file)
        self.button_Combine.setEnabled(False)

        button_Exit = QtWidgets.QPushButton("E&xit")
        button_Exit.setIcon(QtGui.QIcon("icons/exit.png"))
        button_Exit.setFixedHeight(50)
        button_Exit.setToolTip("Exit the application (Alt+X)")
        button_Exit.clicked.connect(self.close)

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
                              self, "Save PDF file as...",
                              os.path.join(self.config.get("save path",
                                                           os.curdir),
                                           self.config.get("save filename",
                                                           "file.pdf")),
                              "PDF files (*.pdf)")
        if output_filename:
            self.config["save path"], self.config["save filename"] \
                                           = os.path.split(output_filename)
            if output_filename in [file_box.filename
                                   for file_box in self.file_boxes]:
                self.message_box(icon=QtWidgets.QMessageBox.Warning,
                                 title="Warning",
                                 text="You are not allowed to overwrite "
                                      "one of the input files.",
                                 informative="Please select a different "
                                             "filename.")
                # to do: dialog
                # Do you really wish to overwrite one of the input files?
            else:
                merger = PyPDF2.PdfFileMerger()
                for file_box in self.file_boxes:
                    filename = file_box.filename
                    if filename:
                        # iterate over "range tuples" and merge as page ranges
                        for range_tuple in file_box.output_tuples:
                            merger.append(filename, pages=range_tuple)
                merger.write(output_filename)
                merger.close()

    def update_main_button(self):
        total_pages = sum([file_box.output_page_count
                           for file_box in self.file_boxes])
        if total_pages > 0:
            self.button_Combine.setText("Combine && &Save {} {}"
                                        .format(total_pages,
                                                "pages" if total_pages > 1
                                                else "page"))
            self.button_Combine.setEnabled(True)
        else:
            self.button_Combine.setText("Combine && &Save")
            self.button_Combine.setEnabled(False)

    def add_item(self):
        file_box = FileBox(parent_app=self, filename="", pages=0,
                           output_tuples=[])
        self.file_boxes.append(file_box)
        self.central_layout.addLayout(file_box.layout)
        line = QtWidgets.QLabel()
        line.setFrameStyle(QtWidgets.QFrame.HLine
                           | QtWidgets.QFrame.Sunken)
        self.central_layout.addWidget(line)

    def help_box(self):
        self.message_box(icon=QtWidgets.QMessageBox.Information,
                         title="Help", text=self.HELP_TEXT)

    def about_box(self):
        self.message_box(icon=QtWidgets.QMessageBox.Information,
                         title="About", text=self.ABOUT_TEXT)

    def run(self, app):
        self.show()
        app.exec_()

    def __del__(self):
        with open("config.json", "w") as file:
            json.dump(self.config, file, indent=4)

    @staticmethod
    def message_box(icon, title, text, detailed="", informative=""):
        message = QtWidgets.QMessageBox(icon, title, text)
        if detailed:
            message.setDetailedText(detailed)
        if informative:
            message.setInformativeText(informative)
        message.exec_()

    # text constants as class variables
    HELP_TEXT = """In the "Pages" input field, enter single page numbers
or ranges of page numbers. Example: 1, 3-5, 8
will produce page sequence 1, 3, 4, 5, 8

Order is observed. Example: 2-4, 1
will produce page sequence 2, 3, 4, 1

Repeating is allowed. Example: 1-3, 2, 1-2
will produce page sequence 1, 2, 3, 2, 1, 2"""

    ABOUT_TEXT = "CombinePDF\n\nversion 0.8.5\n\n3rd February 2018"


def main():
    app = QtWidgets.QApplication()
    app_window = MainWindow()
    app_window.run(app)


if __name__ == "__main__":
    main()
