from mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets as widgests
from PyQt5 import QtCore
from pikepdf import Pdf, PasswordError
import sys


class mainwindow(widgests.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.doc = None

        self.setupUi(self)
        self.actionOpen.triggered.connect(self.open_pdf)
        self.actionSave_as.triggered.connect(self.save_pdf)
        self.actionMerge.triggered.connect(self.merge_pages)
        self.actionRotate.triggered.connect(self.rotate_pages)
        self.actionSplit.triggered.connect(self.split_pages)

    def open_pdf(self):
        path = widgests.QFileDialog.getOpenFileName(
            self, filter="PDF Files (*.pdf)")[0]
        self.pdf = 0
        if path:
            try:
                self.pdf = Pdf.open(path)

            except PasswordError:
                password, ok = widgests.QInputDialog.getText(
                    self, "Your Document is encrypted", f"'{path}' is protected. Please enter a Document Open Password:", widgests.QLineEdit.Password)
                if ok:
                    try:
                        self.pdf = Pdf.open(path, password)
                    except PasswordError:
                        widgests.QMessageBox.warning(
                            self, "Failed!", "Wrong Password")
            except:
                widgests.QMessageBox.warning(self,
                                             "Failed!", "Something went wrong")

    def save_pdf(self):
        output = widgests.QFileDialog.getSaveFileName(
            self, filter="PDF Files (*.pdf)")[0]
        if output:
            with open(output, 'wb') as out:
                self.pdf.save(out)

    def merge_pages(self):
        paths = widgests.QFileDialog.getOpenFileNames(
            self, filter="PDF Files (*.pdf)")[0]
        self.pdf = Pdf.new()
        if paths:
            for path in paths:
                with Pdf.open(path) as temp:
                    self.pdf.pages.extend(temp.pages)
            self.save_pdf()

    def rotate_pages(self):
        self.open_pdf()
        if self.pdf:
            for page in self.pdf.pages:
                # rotiert 90 Grad aber nicht um 90 Grad
                page.rotate = 90
            self.save_pdf()

    def split_pages(self):
        self.open_pdf()
        if self.pdf:
            for page in self.pdf.pages:
                temp = Pdf.new()
                temp.pages.append(page)
                output = widgests.QFileDialog.getSaveFileName(
                    self, filter="PDF Files (*.pdf)")[0]
                if output:
                    temp.save(output)


def main():
    app = widgests.QApplication(sys.argv)
    mw = mainwindow()
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
