import os

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QWidget, QPushButton, QSizePolicy, QVBoxLayout, QFrame, QHBoxLayout


class FindReplaceToolbarWidget(QWidget):
    # searched = pyqtSignal(str, QWebEnginePage.FindFlag)
    replaceSignal = pyqtSignal()
    closeSignal = pyqtSignal()

    def __init__(self, widget, text='', replace_flag=False):
        super().__init__()
        self.__initUi(widget=widget, text=text, replace_flag=replace_flag)

    def __initUi(self, widget, text='', replace_flag=False):
        self.__replace_flag = replace_flag

        self.__widget = widget

        self.__findWidget = FindWidget(self.__widget, text)

        self.__replaceWidget = ReplaceWidget(self.__widget)
        self.__replaceWidget.replaceSignal.connect(self.__sendReplaceSignal)

        find = self.__findWidget.getLineEdit()
        self.setFocusProxy(find)

        if text:
            self.__prepareToReplace(text)
            replace = self.__replaceWidget.getLineEdit()
            self.setFocusProxy(replace)

        self.__findWidget.lineEditSignal.connect(self.__prepareToReplace)

        self.__findWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.__replaceWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        lay = QVBoxLayout()
        lay.addWidget(self.__findWidget)

        if self.__replace_flag:
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setContentsMargins(0, 0, 0, 0)
            line.setMaximumHeight(1)
            lay.addWidget(line)
            lay.addWidget(self.__replaceWidget)

        leftWidget = QWidget()
        leftWidget.setLayout(lay)
        leftWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        swapBtn = QPushButton()
        closeBtn = QPushButton()

        css_file_path = os.path.join(os.path.dirname(os.path.relpath(__file__, os.getcwd())),
                                     r'style/button1.css')
        css_file = open(css_file_path)
        btn_css_code = css_file.read()
        css_file.close()

        swapBtn.setStyleSheet(btn_css_code)
        closeBtn.setStyleSheet(btn_css_code)

        swapBtn.setIcon(QIcon('ico/swap_v.png'))
        closeBtn.setIcon(QIcon('ico/close.png'))

        swapBtn.setToolTip('Find/Replace Text Swap')
        closeBtn.setToolTip('Close')

        swapBtn.clicked.connect(self.__swap)
        closeBtn.clicked.connect(self.__sendCloseSignal)

        lay = QHBoxLayout()
        lay.addWidget(swapBtn)
        lay.addWidget(closeBtn)

        rightWidget = QWidget()
        rightWidget.setLayout(lay)
        rightWidget.setFocusPolicy(Qt.NoFocus)

        lay = QHBoxLayout()
        lay.addWidget(leftWidget)

        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setMaximumWidth(1)
        line.setContentsMargins(0, 0, 0, 0)

        lay.addWidget(line)
        lay.addWidget(rightWidget)

        self.setLayout(lay)

    def __swap(self):
        find_text = self.__findWidget.getLineEdit().text()
        replace_text = self.__replaceWidget.getLineEdit().text()
        self.__findWidget.setLineEdit(replace_text)
        self.__replaceWidget.setLineEdit(find_text)

    def get_find_edit_text(self):
        return self.__findWidget.getLineEdit().text()

    def updateWidget(self, widget):
        self.__widget = widget
        self.__findWidget.updateWidget(self.__widget)
        self.__replaceWidget.updateWidget(self.__widget)

    def __sendReplaceSignal(self):
        self.replaceSignal.emit()
        self.__findWidget.next(replace_flag=True)

    def __prepareToReplace(self, text):
        self.__cursors = self.getCursors(text)
        self.__replaceWidget.setText(self.__cursors)

    def getCursors(self, text):
        cursors = []
        # widget.textCursor().beginEditBlock()
        doc = self.__widget.document()
        cursor = QTextCursor(doc)
        while True:
            cursor = doc.find(text, cursor)
            if cursor.isNull():
                break
            cursors.append(cursor)
        # widget.textCursor().endEditBlock()
        return cursors

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.__sendCloseSignal()
        return super().keyPressEvent(e)

    def __sendCloseSignal(self):
        self.closeSignal.emit()

    def showEvent(self, e):
        self.setFocus(True)
        return super().showEvent(e)

    def setReplaceFlag(self, replace_flag):
        self.__replace_flag = replace_flag
