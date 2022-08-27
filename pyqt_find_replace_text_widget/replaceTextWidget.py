from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout


class ReplaceTextWidget(QWidget):
    replaceSignal = pyqtSignal()

    def __init__(self, widget):
        super().__init__()
        self.__initUi(widget)

    def __initUi(self, widget):
        self.__text_cursors = []
        self.__widget = widget

        self.__replaceLineEdit = QLineEdit()
        self.__replaceLineEdit.setStyleSheet('QLineEdit { border: none; }')

        self.setFocusProxy(self.__replaceLineEdit)

        self.__replaceBtn = QPushButton('Replace')
        self.__replaceAllBtn = QPushButton('Replace All')
        self.__excludeBtn = QPushButton('Exclude')

        self.__btnToggled()

        self.__replaceLineEdit.returnPressed.connect(self.__replace)

        btns = [self.__replaceBtn, self.__replaceAllBtn, self.__excludeBtn]

        self.__replaceBtn.clicked.connect(self.__replace)
        self.__replaceAllBtn.clicked.connect(self.__replaceAll)
        self.__excludeBtn.clicked.connect(self.__exclude)

        lay = QHBoxLayout()
        lay.addWidget(self.__replaceLineEdit)
        for btn in btns:
            lay.addWidget(btn)
        lay.addStretch(0)

        lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lay)

    def updateWidget(self, widget):
        self.__widget = widget

    def setLineEdit(self, text):
        self.__replaceLineEdit.setText(text)

    def getLineEdit(self):
        return self.__replaceLineEdit

    def setText(self, text_cursors):
        self.__text_cursors = text_cursors
        self.__btnToggled()

    def __btnToggled(self):
        f = len(self.__text_cursors) != 0
        self.__replaceBtn.setEnabled(f)
        self.__replaceAllBtn.setEnabled(f)
        self.__excludeBtn.setEnabled(f)

    def __replace(self):
        cur = self.__widget.textCursor()
        if cur:
            old_text = cur.selectedText()
            if old_text:
                new_text = self.__replaceLineEdit.text()
                cur.insertText(new_text)
                self.replaceSignal.emit()

    def __replaceAll(self):
        for text_cursor in self.__text_cursors:
            text_cursor.insertText(self.__replaceLineEdit.text())
            self.__widget.setTextCursor(text_cursor)
        self.replaceSignal.emit()

    def __exclude(self):
        pass
