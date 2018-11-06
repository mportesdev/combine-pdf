#!/usr/bin/python
# coding: utf-8

from PySide2 import QtWidgets, QtCore, QtGui
import os, functools, json, PyPDF2

class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Combine PDF")
        self.resize(640, 400)
        try:
            with open("config.json") as file:
                self.config = json.load(file)
        except:
            self.config = {"Recent open path": os.curdir, "Recent save path": os.curdir, "Number of items": 5}
        self.filenameLabels = []
        self.fileInfo = [{"filename": "", "pages": 0} for i in range(self.config["Number of items"])]
        self.removeButtons = []
        self.pagesEdits = []
        self.pagesLabels = []
        self.messageLabels = []
        helpText = """Order is observed. Example: 2-4, 1
will produce page sequence 2, 3, 4, 1

Repeating is allowed. Example: 1-3, 2, 1-2 will produce page sequence 1, 2, 3, 2, 1, 2

"A" means all pages. Example: A, A
will include the whole document twice"""

        logoImg = QtGui.QImage("icons/logo.png")
        logoLabel = QtWidgets.QLabel()
        logoLabel.setPixmap(QtGui.QPixmap.fromImage(logoImg))
        # buttonHelp = QtWidgets.QPushButton("Help")
        # buttonAbout = QtWidgets.QPushButton("About")
        topLayout = QtWidgets.QGridLayout()
        topLayout.addWidget(logoLabel, 0, 1)
        # topLayout.addWidget(buttonHelp, 0, 3)
        # topLayout.addWidget(buttonAbout, 0, 4)
        topLayout.setColumnStretch(0, 1)
        topLayout.setColumnStretch(1, 3)
        topLayout.setColumnStretch(2, 1)
        topLayout.setColumnStretch(3, 1)
        topLayout.setColumnStretch(4, 1)


        centralLayout = QtWidgets.QGridLayout()
        for i in range(self.config["Number of items"]):
            browseButton = QtWidgets.QPushButton("Select file...")
            browseButton.clicked.connect(functools.partial(self.open_file, i))
            # About using partial to connect slots in a loop:
            # https://stackoverflow.com/questions/40193916/how-come-this-code-only-toggles-blue-python-pyqt
            filenameLabel = QtWidgets.QLabel("[no file]")
            filenameLabel.setEnabled(False)
            self.filenameLabels.append(filenameLabel)
            removeButton = QtWidgets.QPushButton()
            removeButton.setIcon(QtGui.QIcon("icons/trash.png"))
            removeButton.setToolTip("Remove this file")
            removeButton.setFixedWidth(30)
            removeButton.clicked.connect(functools.partial(self.remove_file, i))
            removeButton.setVisible(False)
            self.removeButtons.append(removeButton)
            pagesLabel = QtWidgets.QLabel("Pages:")
            pagesLabel.setAlignment(QtCore.Qt.AlignRight)
            pagesLabel.setVisible(False)
            self.pagesLabels.append(pagesLabel)
            pagesEdit = QtWidgets.QLineEdit()
            pagesEdit.setPlaceholderText("Example: 1, 3-5, 8")
            pagesEdit.setToolTip(helpText)
            pagesEdit.setVisible(False)
            self.pagesEdits.append(pagesEdit)
            messageLabel = QtWidgets.QLabel()
            messageLabel.setVisible(False)
            self.messageLabels.append(messageLabel)
            line = QtWidgets.QLabel()
            line.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Sunken)
            centralLayout.addWidget(browseButton, 5*i + 5, 0)
            centralLayout.addWidget(filenameLabel, 5*i + 5, 1, 1, 3)
            centralLayout.addWidget(removeButton, 5*i + 5, 4)
            centralLayout.addWidget(pagesLabel, 5*i + 6, 0)
            centralLayout.addWidget(pagesEdit, 5*i + 6, 1, 1, 2)
            centralLayout.addWidget(messageLabel, 5*i + 6, 3)
            centralLayout.addWidget(line, 5*i + 8, 0, 1, 5)
        centralLayout.setColumnStretch(1, 3)
        centralLayout.setColumnStretch(3, 4)

        self.buttonCombine = QtWidgets.QPushButton("Combine && Save")
        self.buttonCombine.setIcon(QtGui.QIcon("icons/combine.png"))
        self.buttonCombine.clicked.connect(self.save_file)
        self.buttonCombine.setFixedHeight(50)
        self.buttonCombine.setEnabled(False)
        buttonExit = QtWidgets.QPushButton("Exit")
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
        filenameTuple = QtWidgets.QFileDialog.getOpenFileName(self, "Open a PDF file", self.config["Recent open path"], "PDF files (*.pdf)")
        filename = filenameTuple[0]
        if filename:
            try:
                reader = PyPDF2.PdfFileReader(filename)
                self.fileInfo[n]["pages"] = reader.numPages
                if self.fileInfo[n]["filename"] == "":
                    self.filenameLabels[n].setEnabled(True)
                    self.removeButtons[n].setVisible(True)
                    self.pagesLabels[n].setVisible(True)
                    self.pagesEdits[n].setVisible(True)
                    self.messageLabels[n].setVisible(True)
                self.fileInfo[n]["filename"] = filename
                self.config["Recent open path"] = os.path.split(filename)[0]
                self.filenameLabels[n].setText(os.path.basename(filename))
                self.filenameLabels[n].setToolTip("{} ({} {})".format(filename, self.fileInfo[n]["pages"], "pages" if self.fileInfo[n]["pages"] > 1 else "page"))
                self.refresh_button()
            except:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setText("File could not be read.")
                msg.exec_()

    def remove_file(self, n):
        self.filenameLabels[n].setText("[no file]")
        self.filenameLabels[n].setEnabled(False)
        self.filenameLabels[n].setToolTip("")
        self.fileInfo[n]["filename"] = ""
        self.fileInfo[n]["pages"] = 0
        self.removeButtons[n].setVisible(False)
        self.pagesLabels[n].setVisible(False)
        self.pagesEdits[n].setVisible(False)
        self.messageLabels[n].setVisible(False)
        self.refresh_button()

    def save_file(self):
        outputFilenameTuple = QtWidgets.QFileDialog.getSaveFileName(self, "Save PDF file as...", self.config["Recent save path"], "PDF files (*.pdf)")
        outputFilename = outputFilenameTuple[0]
        if outputFilename:
            if outputFilename in [item["filename"] for item in self.fileInfo]:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setText("You are not allowed to overwrite one of the input files.")
                msg.exec_()
                # to do 2: Dialog: Do you really wish to overwrite one of the input files?
            else:
                self.config["Recent save path"] = os.path.split(outputFilename)[0]
                merger = PyPDF2.PdfFileMerger()
                for filename in [item["filename"] for item in self.fileInfo]:
                    if filename:
                        merger.append(filename)
                merger.write(outputFilename)
                merger.close()

    def refresh_button(self):
        totalPages = sum([self.fileInfo[i]["pages"] for i in range(self.config["Number of items"])])
        if totalPages > 0:
            self.buttonCombine.setText("Combine && Save {} {}".format(totalPages, "pages" if totalPages > 1 else "page"))
            self.buttonCombine.setEnabled(True)
        else:
            self.buttonCombine.setText("Combine && Save")
            self.buttonCombine.setEnabled(False)

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
