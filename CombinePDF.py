#!/usr/bin/python
# coding: utf-8

from PySide2 import QtWidgets, QtGui
import os
import json
import PyPDF2


class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CombinePDF")
        self.resize(640, 400)
        try:
            with open("config.json") as file:
                self.config = json.load(file)
        except FileNotFoundError:
            self.config = {"Recent open path": os.curdir,
                           "Recent save path": os.curdir,
                           "Recent save name": "file.pdf",
                           "Number of items": 5}
        self.file_info = [{"filename": "", "pages": 0, "output": []}
                          for _ in range(self.config["Number of items"])]
        self.filename_labels = []
        self.pages_infos = []
        self.remove_buttons = []
        self.rbuttons_All = []
        self.rbuttons_Pages = []
        self.rbutton_groups = []
        self.page_select_edits = []
        self.page_select_infos = []

        logo_img = QtGui.QImage("icons/logo.png")
        logo_label = QtWidgets.QLabel()
        logo_label.setPixmap(QtGui.QPixmap.fromImage(logo_img))
        button_Help = QtWidgets.QPushButton()
        button_Help.setIcon(QtGui.QIcon("icons/question.png"))
        button_Help.setFixedWidth(30)
        button_Help.setToolTip("Help")
        button_Help.clicked.connect(self.help_box)
        button_About = QtWidgets.QPushButton()
        button_About.setIcon(QtGui.QIcon("icons/info.png"))
        button_About.setFixedWidth(30)
        button_About.setToolTip("About")
        button_About.clicked.connect(self.about_box)
        top_layout = QtWidgets.QGridLayout()
        top_layout.addWidget(logo_label, 0, 1)
        top_layout.addWidget(button_Help, 0, 3)
        top_layout.addWidget(button_About, 0, 4)
        top_layout.setColumnStretch(0, 1)
        top_layout.setColumnStretch(1, 3)
        top_layout.setColumnStretch(2, 1)
        top_layout.setColumnStretch(3, 1)
        top_layout.setColumnStretch(4, 1)

        central_layout = QtWidgets.QGridLayout()
        line = QtWidgets.QLabel()
        line.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Sunken)
        central_layout.addWidget(line, 0, 0, 1, 5)
        for i in range(self.config["Number of items"]):
            button_Browse = QtWidgets.QPushButton("Select file...")
            button_Browse.clicked[bool].connect(lambda *args, item=i:
                                                self.open_file(item))
            filename_label = QtWidgets.QLabel("[no file]")
            filename_label.setEnabled(False)
            self.filename_labels.append(filename_label)
            pages_info = QtWidgets.QLabel()
            pages_info.setStyleSheet("color: #477b6e")
            self.pages_infos.append(pages_info)
            button_Remove = QtWidgets.QPushButton()
            button_Remove.setIcon(QtGui.QIcon("icons/trash.png"))
            button_Remove.setToolTip("Remove this file")
            button_Remove.setFixedWidth(30)
            button_Remove.clicked.connect(lambda *args, item=i:
                                          self.remove_file(item))
            button_Remove.clicked.connect(self.update_main_button)
            button_Remove.setVisible(False)
            self.remove_buttons.append(button_Remove)

            rbutton_All = QtWidgets.QRadioButton("All")
            rbutton_All.toggled.connect(lambda *args, item=i:
                                        self.switch_rbuttons(item))
            rbutton_All.toggled.connect(self.update_main_button)
            rbutton_All.setVisible(False)
            self.rbuttons_All.append(rbutton_All)
            rbutton_Pages = QtWidgets.QRadioButton("Pages")
            rbutton_Pages.setVisible(False)
            self.rbuttons_Pages.append(rbutton_Pages)
            rbutton_group = QtWidgets.QButtonGroup()
            rbutton_group.addButton(rbutton_All)
            rbutton_group.addButton(rbutton_Pages)
            self.rbutton_groups.append(rbutton_group)
            page_select_edit = QtWidgets.QLineEdit()
            page_select_edit.setPlaceholderText("Example: 1, 3-5, 8")
            page_select_edit.textEdited.connect(lambda *args, item=i:
                                                self.update_select_info(item))
            page_select_edit.textEdited.connect(self.update_main_button)
            page_select_edit.setVisible(False)
            self.page_select_edits.append(page_select_edit)
            page_select_info = QtWidgets.QLabel()
            page_select_info.setVisible(False)
            page_select_info.setStyleSheet("color: #477b6e")
            self.page_select_infos.append(page_select_info)
            spacer = QtWidgets.QSpacerItem(30, 0)

            line = QtWidgets.QLabel()
            line.setFrameStyle(QtWidgets.QFrame.HLine
                               | QtWidgets.QFrame.Sunken)

            central_layout.addWidget(button_Browse, 5*i + 1, 0)
            central_layout.addWidget(filename_label, 5*i + 1, 1, 1, 3)
            central_layout.addWidget(pages_info, 5*i + 1, 4)
            central_layout.addWidget(button_Remove, 5*i + 1, 5)
            central_layout.addWidget(rbutton_All, 5*i + 2, 1)
            central_layout.addWidget(rbutton_Pages, 5*i + 2, 2)
            central_layout.addWidget(page_select_edit, 5*i + 2, 3)
            central_layout.addWidget(page_select_info, 5*i + 2, 4)
            central_layout.addItem(spacer, 5*i + 2, 5)
            central_layout.addWidget(line, 5*i + 3, 0, 1, 5)

            # only for column width testing:
            # filename_label.setStyleSheet("background: #ddd")
            # pages_info.setStyleSheet("background: #ddd")
            # pages_info.setStyleSheet("background: #ddd")
            # rbutton_All.setStyleSheet("background: #ddd")
            # rbutton_Pages.setStyleSheet("background: #ddd")
            # page_select_info.setStyleSheet("background: #ddd")

        for i in range(1, 5):
            central_layout.setColumnStretch(i, (10, 10, 55, 25)[i-1])

        self.button_Combine = QtWidgets.QPushButton("Combine && &Save")
        self.button_Combine.setIcon(QtGui.QIcon("icons/combine.png"))
        self.button_Combine.clicked.connect(self.save_file)
        self.button_Combine.setFixedHeight(50)
        self.button_Combine.setEnabled(False)
        button_Exit = QtWidgets.QPushButton("E&xit")
        button_Exit.setIcon(QtGui.QIcon("icons/exit.png"))
        button_Exit.clicked.connect(self.close)
        button_Exit.setFixedHeight(50)
        bottom_layout = QtWidgets.QGridLayout()
        bottom_layout.addWidget(self.button_Combine, 0, 1)
        bottom_layout.addWidget(button_Exit, 0, 2)
        bottom_layout.setColumnStretch(0, 1)
        bottom_layout.setColumnStretch(1, 3)
        bottom_layout.setColumnStretch(2, 1)
        bottom_layout.setColumnStretch(3, 1)

        master_layout = QtWidgets.QVBoxLayout()
        master_layout.addLayout(top_layout)
        master_layout.addLayout(central_layout)
        master_layout.addLayout(bottom_layout)
        self.setLayout(master_layout)

    def open_file(self, n):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
                      self,
                      "Open a PDF file",
                      self.config["Recent open path"],
                      "PDF files (*.pdf)")
        if filename:
            self.config["Recent open path"] = os.path.split(filename)[0]
            try:
                reader = PyPDF2.PdfFileReader(filename)
                pages = reader.numPages
            except Exception as err:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("File could not be read.")
                msg.setDetailedText("File: {}\n\nError: {}"
                                    .format(filename, err))
                msg.exec_()
            else:
                if self.file_info[n]["filename"] == "":
                    self.filename_labels[n].setEnabled(True)
                    self.remove_buttons[n].setVisible(True)
                    self.rbuttons_All[n].setVisible(True)
                    self.rbuttons_Pages[n].setVisible(True)
                    self.page_select_edits[n].setVisible(True)
                self.file_info[n]["filename"] = filename
                self.file_info[n]["pages"] = pages
                # output after opening the file:
                self.file_info[n]["output"] = [(0, pages)]
                self.filename_labels[n].setText(os.path.basename(filename))
                self.filename_labels[n].setToolTip(filename)
                self.rbuttons_All[n].setChecked(True)
                self.pages_infos[n].setText("{} {} total".format(pages,
                                            "pages" if pages > 1 else "page"))
                self.page_select_edits[n].setText("")
                self.page_select_infos[n].setText("nothing selected")

    def remove_file(self, n):
        self.file_info[n]["filename"] = ""
        self.file_info[n]["pages"] = 0
        self.file_info[n]["output"] = []
        self.filename_labels[n].setText("[no file]")
        self.filename_labels[n].setEnabled(False)
        self.filename_labels[n].setToolTip("")
        self.pages_infos[n].setText("")
        self.remove_buttons[n].setVisible(False)
        self.rbuttons_All[n].setVisible(False)
        self.rbuttons_Pages[n].setVisible(False)
        self.page_select_edits[n].setVisible(False)
        self.page_select_infos[n].setVisible(False)

    def save_file(self):
        output_filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                            self,
                            "Save PDF file as...",
                            os.path.join(self.config["Recent save path"],
                                         self.config["Recent save name"]),
                            "PDF files (*.pdf)")
        if output_filename:
            self.config["Recent save path"] = os.path.split(output_filename)[0]
            if output_filename in [item["filename"]
                                   for item in self.file_info]:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("You are not allowed to overwrite "
                            "one of the input files.")
                msg.setInformativeText("Please select a different filename.")
                msg.exec_()
                # to do 2: Dialog: Do you really wish to overwrite
                # one of the input files?
            else:
                merger = PyPDF2.PdfFileMerger()
                for item in self.file_info:
                    filename = item["filename"]
                    if filename:
                        # iterate over "range tuples" and merge as page ranges
                        for range_tuple in item["output"]:
                            print("Appending {} of {}.".format(range_tuple,
                                                               filename))
                            merger.append(filename, pages=range_tuple)
                merger.write(output_filename)
                merger.close()

    def update_select_info(self, n):
        self.file_info[n]["output"], valid = self.string_to_range_tuples(
                                            self.page_select_edits[n].text(),
                                            self.file_info[n]["pages"])
        if valid:
            selection = self.range_tuples_to_page_count(
                        self.file_info[n]["output"])
            self.page_select_infos[n].setText(
                "{} {} selected".format(selection,
                                        "pages" if selection > 1 else "page"))
        else:
            self.page_select_infos[n].setText("selection not valid")
        print("output from evaluating page_select_edit:",
              self.file_info[n]["output"])

    def string_to_range_tuples(self, user_string, last_page):
        result = []
        valid = True
        if user_string:
            for part in user_string.split(","):
                try:
                    # valid single page number?
                    from_page = int(part.strip())
                except ValueError:
                    # not a valid single number
                    try:
                        # valid range of page numbers?
                        from_page = int(part.split("-")[0].strip())
                        to_page = int(part.split("-", 1)[1].strip())
                    except ValueError:
                        # not a valid range of numbers
                        valid = False
                        break
                    else:
                        # valid range of numbers
                        if 1 <= from_page <= last_page and \
                           1 <= to_page <= last_page:
                            # we have a range of valid page numbers -> make a
                            # tuple to be directly used by merger.append()
                            # (pages numbered from 0)
                            range_tuple = (from_page - 1, to_page)
                        else:
                            # range of numbers out of page range
                            valid = False
                            break
                else:
                    # valid single number
                    if 1 <= from_page <= last_page:
                        # we have a valid page number -> make a tuple to be
                        # directly used by merger.append()
                        # (pages numbered from 0)
                        range_tuple = (from_page - 1, from_page)
                    else:
                        # number out of page range
                        valid = False
                        break
                result.append(range_tuple)
        if result and valid:
            return result, valid
        else:
            return [], False

    def range_tuples_to_page_count(self, range_tuples):
        result = 0
        for tup in range_tuples:
            result += len(range(*tup))
        return result

    def update_main_button(self):
        # calculated total pages to merge:
        pages = sum([self.range_tuples_to_page_count(
                     self.file_info[i]["output"])
                     for i in range(self.config["Number of items"])])
        if pages > 0:
            self.button_Combine.setText("Combine && &Save {} {}".format(pages,
                                        "pages" if pages > 1 else "page"))
            self.button_Combine.setEnabled(True)
        else:
            self.button_Combine.setText("Combine && &Save")
            self.button_Combine.setEnabled(False)

    def switch_rbuttons(self, n):
        if self.rbuttons_All[n].isChecked():
            self.file_info[n]["output"] = [(0, self.file_info[n]["pages"])]
            print("output after checking 'All':", self.file_info[n]["output"])
            self.page_select_edits[n].setEnabled(False)
            self.page_select_infos[n].setVisible(False)
        else:
            self.update_select_info(n)
            print("output after checking 'Pages':", self.file_info[n]["output"])
            self.page_select_edits[n].setEnabled(True)
            self.page_select_edits[n].setFocus()
            self.page_select_infos[n].setVisible(True)

    def help_box(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Help")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("""In the "Pages" input field, you can enter single page numbers
and ranges of page numbers. Example: 1, 3-5, 8
will produce page sequence 1, 3, 4, 5, 8

Order is observed. Example: 2-4, 1
will produce page sequence 2, 3, 4, 1

Repeating is allowed. Example: 1-3, 2, 1-2
will produce page sequence 1, 2, 3, 2, 1, 2""")

# "A" means all pages. Example: A, A
# will include the whole document twice

        msg.exec_()

    def about_box(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("About")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("""CombinePDF

version 0.8

6th December 2018""")
        msg.exec_()

    def run(self, app):
        self.show()
        app.exec_()

    def __del__(self):
        with open("config.json", "w") as file:
            json.dump(self.config, file, indent=4)


def main():
    app = QtWidgets.QApplication()
    app_window = MainWindow()
    app_window.run(app)


if __name__ == "__main__":
    main()
