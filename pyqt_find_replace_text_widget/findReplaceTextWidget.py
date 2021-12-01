import os

from PyQt5.QtGui import QTextCursor, QIcon
from PyQt5.QtWidgets import QWidget, QTextEdit, QApplication, QVBoxLayout, QHBoxLayout, QPushButton
from pyqt_find_text_widget.findTextWidget import FindTextWidget

from pyqt_find_replace_text_widget.replaceTextWidget import ReplaceTextWidget


class FindReplaceTextWidget(QWidget):
    def __init__(self, widget):
        super().__init__()
        self.__widget = widget
        self.__initUi()

    def __initUi(self):
        self.__findTextWidget = FindTextWidget(self.__widget)
        self.__replaceTextWidget = ReplaceTextWidget(self.__widget)
        self.__replaceTextWidget.replaceSignal.connect(self.__findTextWidget.next)

        findTextLineEdit = self.__findTextWidget.getLineEdit()
        findTextLineEdit.textChanged.connect(self.__prepareToReplaceFoundText)

        lay = QVBoxLayout()
        lay.addWidget(self.__findTextWidget)
        lay.addWidget(self.__replaceTextWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        leftWidget = QWidget()
        leftWidget.setLayout(lay)

        swapBtn = QPushButton()
        swapBtn.clicked.connect(self.__swap)

        closeBtn = QPushButton()
        closeBtn.setShortcut('Escape')
        closeBtn.clicked.connect(self.__close)

        rel_dirname = os.path.dirname(os.path.relpath(__file__, os.getcwd()))

        css_file_path = os.path.join(rel_dirname, r'style/button2.css')
        css_file = open(css_file_path)
        btn_css_code = css_file.read()
        css_file.close()

        swapBtn.setStyleSheet(btn_css_code)
        closeBtn.setStyleSheet(btn_css_code)

        swapBtn.setIcon(QIcon(os.path.join(rel_dirname, r'ico/swap_v.png')))
        closeBtn.setIcon(QIcon(os.path.join(rel_dirname, r'ico/close.png')))

        swapBtn.setToolTip('Swap Find/Replace Text')
        closeBtn.setToolTip('Close')

        lay = QHBoxLayout()
        lay.addWidget(swapBtn)
        lay.addWidget(closeBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        rightWidget = QWidget()
        rightWidget.setLayout(lay)

        lay = QHBoxLayout()
        lay.addWidget(leftWidget)
        lay.addWidget(rightWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

    def __prepareToReplaceFoundText(self, text):
        cursors = []
        if text:
            doc = self.__widget.document()
            cursor = QTextCursor(doc)
            while True:
                cursor = doc.find(text, cursor)
                if cursor.isNull():
                    break
                cursors.append(cursor)
        self.__replaceTextWidget.setText(cursors)

    def __swap(self):
        find_text = self.__findTextWidget.getLineEdit().text()
        replace_text = self.__replaceTextWidget.getLineEdit().text()
        self.__findTextWidget.setLineEdit(replace_text)
        self.__replaceTextWidget.setLineEdit(find_text)

    def __close(self):
        self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    findReplaceTextWidget = FindReplaceTextWidget()
    findReplaceTextWidget.show()
    app.exec_()