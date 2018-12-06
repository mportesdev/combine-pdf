#!/usr/bin/python
# coding: utf-8

from PySide2 import QtWidgets, QtCore, QtGui
import os, json, PyPDF2

class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CombinePDF")
        self.resize(640, 400)
        try:
            with open("config.json") as file:
                self.config = json.load(file)
        except:
            self.config = {"Recent open path": os.curdir,
                           "Recent save path": os.curdir,
                           "Number of items": 5}
        self.fileInfo = [{"filename": "", "pages": 0, "output": []} for _ in range(self.config["Number of items"])]
        self.filenameLabels = []
        self.pagesInfos = []
        self.removeButtons = []
        self.rbuttonsAll = []
        self.rbuttonsPages = []
        self.rbuttonGroups = []
        self.pageSelectEdits = []
        self.pageSelectInfos = []

        logoImg = QtGui.QImage("icons/logo.png")
        logoLabel = QtWidgets.QLabel()
        logoLabel.setPixmap(QtGui.QPixmap.fromImage(logoImg))
        buttonHelp = QtWidgets.QPushButton()
        buttonHelp.setIcon(QtGui.QIcon("icons/question.png"))
        buttonHelp.setFixedWidth(30)
        buttonHelp.setToolTip("Help")
        buttonHelp.clicked.connect(self.help_box)
        buttonAbout = QtWidgets.QPushButton()
        buttonAbout.setIcon(QtGui.QIcon("icons/info.png"))
        buttonAbout.setFixedWidth(30)
        buttonAbout.setToolTip("About")
        buttonAbout.clicked.connect(self.about_box)
        topLayout = QtWidgets.QGridLayout()
        topLayout.addWidget(logoLabel, 0, 1)
        topLayout.addWidget(buttonHelp, 0, 3)
        topLayout.addWidget(buttonAbout, 0, 4)
        topLayout.setColumnStretch(0, 1)
        topLayout.setColumnStretch(1, 3)
        topLayout.setColumnStretch(2, 1)
        topLayout.setColumnStretch(3, 1)
        topLayout.setColumnStretch(4, 1)

        centralLayout = QtWidgets.QGridLayout()
        line = QtWidgets.QLabel()
        line.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Sunken)
        centralLayout.addWidget(line, 0, 0, 1, 5)
        for i in range(self.config["Number of items"]):
            browseButton = QtWidgets.QPushButton("Select file...")
            browseButton.clicked[bool].connect(lambda *args, item=i: self.open_file(item))
            filenameLabel = QtWidgets.QLabel("[no file]")
            filenameLabel.setEnabled(False)
            self.filenameLabels.append(filenameLabel)
            pagesInfo = QtWidgets.QLabel()
            pagesInfo.setStyleSheet("color: #477b6e")
            self.pagesInfos.append(pagesInfo)
            removeButton = QtWidgets.QPushButton()
            removeButton.setIcon(QtGui.QIcon("icons/trash.png"))
            removeButton.setToolTip("Remove this file")
            removeButton.setFixedWidth(30)
            removeButton.clicked.connect(lambda *args, item=i: self.remove_file(item))
            removeButton.clicked.connect(self.update_main_button)
            removeButton.setVisible(False)
            self.removeButtons.append(removeButton)

            rbuttonAll = QtWidgets.QRadioButton("All")
            rbuttonAll.toggled.connect(lambda *args, item=i: self.switch_rbuttons(item))
            rbuttonAll.toggled.connect(self.update_main_button)
            rbuttonAll.setVisible(False)
            self.rbuttonsAll.append(rbuttonAll)
            rbuttonPages = QtWidgets.QRadioButton("Pages")
            rbuttonPages.setVisible(False)
            self.rbuttonsPages.append(rbuttonPages)
            rbuttonGroup = QtWidgets.QButtonGroup()
            rbuttonGroup.addButton(rbuttonAll)
            rbuttonGroup.addButton(rbuttonPages)
            self.rbuttonGroups.append(rbuttonGroup)
            pageSelectEdit = QtWidgets.QLineEdit()
            pageSelectEdit.setPlaceholderText("Example: 1, 3-5, 8")
            pageSelectEdit.textEdited.connect(lambda *args, item=i: self.update_select_info(item))
            pageSelectEdit.textEdited.connect(self.update_main_button)
            pageSelectEdit.setVisible(False)
            self.pageSelectEdits.append(pageSelectEdit)
            pageSelectInfo = QtWidgets.QLabel()
            pageSelectInfo.setVisible(False)
            pageSelectInfo.setStyleSheet("color: #477b6e")
            self.pageSelectInfos.append(pageSelectInfo)
            spacer = QtWidgets.QSpacerItem(30, 0)

            line = QtWidgets.QLabel()
            line.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Sunken)

            centralLayout.addWidget(browseButton, 5*i + 1, 0)
            centralLayout.addWidget(filenameLabel, 5*i + 1, 1, 1, 3)
            centralLayout.addWidget(pagesInfo, 5*i + 1, 4)
            centralLayout.addWidget(removeButton, 5*i + 1, 5)
            centralLayout.addWidget(rbuttonAll, 5*i + 2, 1)
            centralLayout.addWidget(rbuttonPages, 5*i + 2, 2)
            centralLayout.addWidget(pageSelectEdit, 5*i + 2, 3)
            centralLayout.addWidget(pageSelectInfo, 5*i + 2, 4)
            centralLayout.addItem(spacer, 5*i + 2, 5)
            centralLayout.addWidget(line, 5*i + 3, 0, 1, 5)

            ### only for column width testing:
            # filenameLabel.setStyleSheet("background: #ddd")
            # pagesInfo.setStyleSheet("background: #ddd")
            # pagesInfo.setStyleSheet("background: #ddd")
            # rbuttonAll.setStyleSheet("background: #ddd")
            # rbuttonPages.setStyleSheet("background: #ddd")
            # pageSelectInfo.setStyleSheet("background: #ddd")

        for i in range(1, 5):
            centralLayout.setColumnStretch(i, (10, 10, 55, 25)[i-1])

        self.buttonCombine = QtWidgets.QPushButton("Combine && &Save")
        self.buttonCombine.setIcon(QtGui.QIcon("icons/combine.png"))
        self.buttonCombine.clicked.connect(self.save_file)
        self.buttonCombine.setFixedHeight(50)
        self.buttonCombine.setEnabled(False)
        buttonExit = QtWidgets.QPushButton("E&xit")
        buttonExit.setIcon(QtGui.QIcon("icons/exit.png"))
        buttonExit.clicked.connect(self.close)
        buttonExit.setFixedHeight(50)
        bottomLayout = QtWidgets.QGridLayout()
        bottomLayout.addWidget(self.buttonCombine, 0, 1)
        bottomLayout.addWidget(buttonExit, 0, 2)
        bottomLayout.setColumnStretch(0, 1)
        bottomLayout.setColumnStretch(1, 3)
        bottomLayout.setColumnStretch(2, 1)
        bottomLayout.setColumnStretch(3, 1)

        masterLayout = QtWidgets.QVBoxLayout()
        masterLayout.addLayout(topLayout)
        masterLayout.addLayout(centralLayout)
        masterLayout.addLayout(bottomLayout)
        self.setLayout(masterLayout)

    def open_file(self, n):
        filenameTuple = QtWidgets.QFileDialog.getOpenFileName(self, "Open a PDF file",
                                                              self.config["Recent open path"],
                                                              "PDF files (*.pdf)")
        filename = filenameTuple[0]
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
                msg.setDetailedText("File: {}\n\nError: {}".format(filename, err))
                msg.exec_()
            else:
                if self.fileInfo[n]["filename"] == "":
                    self.filenameLabels[n].setEnabled(True)
                    self.removeButtons[n].setVisible(True)
                    self.rbuttonsAll[n].setVisible(True)
                    self.rbuttonsPages[n].setVisible(True)
                    self.pageSelectEdits[n].setVisible(True)
                self.fileInfo[n]["filename"] = filename
                self.fileInfo[n]["pages"] = pages
                ### output after opening the file:
                self.fileInfo[n]["output"] = [(0, pages)]
                self.filenameLabels[n].setText(os.path.basename(filename))
                self.filenameLabels[n].setToolTip(filename)
                self.rbuttonsAll[n].setChecked(True)
                self.pagesInfos[n].setText("{} {} total".format(pages, "pages" if pages > 1 else "page"))
                self.pageSelectEdits[n].setText("")
                self.pageSelectInfos[n].setText("nothing selected")

    def remove_file(self, n):
        self.fileInfo[n]["filename"] = ""
        self.fileInfo[n]["pages"] = 0
        self.fileInfo[n]["output"] = []
        self.filenameLabels[n].setText("[no file]")
        self.filenameLabels[n].setEnabled(False)
        self.filenameLabels[n].setToolTip("")
        self.pagesInfos[n].setText("")
        self.removeButtons[n].setVisible(False)
        self.rbuttonsAll[n].setVisible(False)
        self.rbuttonsPages[n].setVisible(False)
        self.pageSelectEdits[n].setVisible(False)
        self.pageSelectInfos[n].setVisible(False)

    def save_file(self):
        outputFilenameTuple = QtWidgets.QFileDialog.getSaveFileName(self, "Save PDF file as...",
                                                                    self.config["Recent save path"],
                                                                    "PDF files (*.pdf)")
        outputFilename = outputFilenameTuple[0]
        if outputFilename:
            self.config["Recent save path"] = os.path.split(outputFilename)[0]
            if outputFilename in [item["filename"] for item in self.fileInfo]:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("You are not allowed to overwrite one of the input files.")
                msg.setInformativeText("Please select a different filename.")
                msg.exec_()
                ### to do 2: Dialog: Do you really wish to overwrite one of the input files?
            else:
                merger = PyPDF2.PdfFileMerger()
                for filename in [item["filename"] for item in self.fileInfo]:
                    if filename:
                        ### to do: iterate over "range tuples" and merge as page ranges
                        merger.append(filename)
                merger.write(outputFilename)
                merger.close()

    def update_select_info(self, n):
        self.fileInfo[n]["output"], valid = self.string_to_range_tuples(self.pageSelectEdits[n].text(), self.fileInfo[n]["pages"])
        if valid:
            selection = self.range_tuples_to_page_count(self.fileInfo[n]["output"])
            self.pageSelectInfos[n].setText("{} {} selected".format(selection, "pages" if selection > 1 else "page"))
        else:
            self.pageSelectInfos[n].setText("selection not valid")
        print("output from evaluating pageSelectEdit:", self.fileInfo[n]["output"])

    def string_to_range_tuples(self, user_string, last_page):
        result = []
        valid = True
        if user_string:
            for part in user_string.split(","):
                try:
                    ### valid single page number?
                    fromPage = int(part.strip())
                except:
                    ### not a valid single number
                    try:
                        ### valid range of page numbers?
                        fromPage = int(part.split("-")[0].strip())
                        toPage = int(part.split("-", 1)[1].strip())
                    except:
                        ### not a valid range of numbers
                        valid = False
                        break
                    else:
                        ### valid range of numbers
                        if 1 <= fromPage <= last_page and 1 <= toPage <= last_page:
                            ### we have a range of valid page numbers -> make a
                            ### tuple to be directly used by merger.append()
                            ### (page numbered from 0)
                            range_tuple = (fromPage - 1, toPage)
                        else:
                            ### range of numbers out of page range
                            valid = False
                            break
                else:
                    ### valid single number
                    if 1 <= fromPage <= last_page:
                        ### we have a valid page number -> make a tuple to be
                        ### directly used by merger.append()
                        ### (page numbered from 0)
                        range_tuple = (fromPage - 1, fromPage)
                    else:
                        ### number out of page range
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
        ### calculated total pages to merge:
        pages = sum([self.range_tuples_to_page_count(self.fileInfo[i]["output"]) for i in range(self.config["Number of items"])])
        if pages > 0:
            self.buttonCombine.setText("Combine && &Save {} {}".format(pages, "pages" if pages > 1 else "page"))
            self.buttonCombine.setEnabled(True)
        else:
            self.buttonCombine.setText("Combine && &Save")
            self.buttonCombine.setEnabled(False)

    def switch_rbuttons(self, n):
        if self.rbuttonsAll[n].isChecked():
            self.fileInfo[n]["output"] = [(0, self.fileInfo[n]["pages"])]
            print("output after checking 'All':", self.fileInfo[n]["output"])
            self.pageSelectEdits[n].setEnabled(False)
            self.pageSelectInfos[n].setVisible(False)
        else:
            self.update_select_info(n)
            print("output after checking 'Pages':", self.fileInfo[n]["output"])
            self.pageSelectEdits[n].setEnabled(True)
            self.pageSelectEdits[n].setFocus()
            self.pageSelectInfos[n].setVisible(True)

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
    appWindow = MainWindow()
    appWindow.run(app)

if __name__ == "__main__":
    main()
