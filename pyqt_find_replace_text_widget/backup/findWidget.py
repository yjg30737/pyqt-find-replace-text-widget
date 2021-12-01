import os

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QTextDocument, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt


class FindWidget(QWidget):
    lineEditSignal = pyqtSignal(str)

    def __init__(self, widget, text=''):
        super().__init__()
        self.__initUi(widget, text)

    def __initUi(self, widget, text):
        self.__widget = widget

        self.__prev_btn = QPushButton()
        self.__next_btn = QPushButton()

        self.__case_btn = QPushButton()
        self.__case_btn.setCheckable(True)

        self.__regex_btn = QPushButton()
        self.__regex_btn.setCheckable(True)

        btns = [self.__prev_btn, self.__next_btn, self.__case_btn, self.__regex_btn]

        css_file_path = os.path.join(os.path.dirname(os.path.relpath(__file__, os.getcwd())),
                                     r'style/button1.css')
        css_file = open(css_file_path)
        btn_css_code = css_file.read()
        css_file.close()

        for btn in btns:
            btn.setStyleSheet(btn_css_code)

        self.__prev_btn.setIcon(QIcon('ico/prev.png'))
        self.__next_btn.setIcon(QIcon('ico/next.png'))
        self.__case_btn.setIcon(QIcon('ico/case.png'))
        self.__regex_btn.setIcon(QIcon('ico/regex.png'))

        self.__prev_btn.setToolTip('Prev Occurrence')
        self.__next_btn.setToolTip('Next Occurrence')
        self.__case_btn.setToolTip('Match Case')
        self.__regex_btn.setToolTip('Regex')

        self.__findLineEdit = QLineEdit()

        if text:
            self.__findLineEdit.setText(text)
        self.setFocusProxy(self.__findLineEdit)

        self.__cnt_lbl = QLabel('0 results')
        self.__cnt_lbl.setFont(QFont('Arial', 7))

        self.__prev_btn.clicked.connect(self.__prev)
        self.__next_btn.clicked.connect(self.next)
        self.__case_btn.clicked.connect(self.__updateSearching)
        self.__regex_btn.clicked.connect(self.__regex)

        self.__updateSearching()

        self.__findLineEdit.textChanged.connect(self.__updateSearching)
        self.__findLineEdit.returnPressed.connect(self.next)

        lay = QHBoxLayout()
        lay.addWidget(self.__findLineEdit)
        lay.addWidget(self.__cnt_lbl)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setContentsMargins(0, 0, 0, 0)
        line.setMaximumHeight(1)
        lay.addWidget(line)

        for btn in btns:
            lay.addWidget(btn)
            btn.setFocusPolicy(Qt.NoFocus)

        self.setLayout(lay)

    def __regex(self):
        pass

    def setLineEdit(self, text):
        self.__findLineEdit.setText(text)

    def getLineEdit(self):
        return self.__findLineEdit

    def updateWidget(self, widget):
        self.__widget = widget
        self.__updateSearching()

    @pyqtSlot()
    def __updateSearching(self):
        text = self.__findLineEdit.text()
        flag = (text.strip() != '')
        self.__prev_btn.setEnabled(flag)
        self.__next_btn.setEnabled(flag)
        TextWidgetHelper.setAll(self.__widget, text)
        if flag:
            word_cnt = TextWidgetHelper.getCountOfWord(self.__widget, text)
            self.__cnt_lbl.setText(str(word_cnt) + str('개의 결과'))
            self.lineEditSignal.emit(text)
        else:
            self.__cnt_lbl.setText('0개의 결과')

    def __prev(self):
        text = self.__findLineEdit.text()
        if text.strip() != '':
            if self.__case_btn.isChecked():
                TextWidgetHelper.setPrev(self.__widget, text, QTextDocument.FindCaseSensitively)
            else:
                TextWidgetHelper.setPrev(self.__widget, text)

    def next(self, replace_flag=False):
        text = self.__findLineEdit.text()
        if text.strip() != '':
            if self.__case_btn.isChecked():
                TextWidgetHelper.setNext(self.__widget, text, QTextDocument.FindCaseSensitively, replace_flag=replace_flag)
            else:
                TextWidgetHelper.setNext(self.__widget, text, replace_flag=replace_flag)
