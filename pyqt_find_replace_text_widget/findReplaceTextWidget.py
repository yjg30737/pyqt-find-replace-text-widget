from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from pyqt_find_text_widget.findTextWidget import FindTextWidget

from pyqt_find_replace_text_widget.replaceTextWidget import ReplaceTextWidget
from pyqt_resource_helper.pyqtResourceHelper import PyQtResourceHelper


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
        self.setFocusProxy(findTextLineEdit)

        self.__widget.textChanged.connect(self.__findTextWidget.widgetTextChanged)

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
        closeBtn.clicked.connect(self.close)

        btns = [swapBtn, closeBtn]

        PyQtResourceHelper.setStyleSheet(btns, ['style/button2.css']*2)
        PyQtResourceHelper.setIcon(btns, ['ico/swap_v.png', 'ico/close.png'])

        swapBtn.setToolTip('Swap Find/Replace Text')
        closeBtn.setToolTip('Close')

        lay = QHBoxLayout()
        lay.addWidget(swapBtn)
        lay.addWidget(closeBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        self.__rightWidget = QWidget()
        self.__rightWidget.setLayout(lay)

        lay = QHBoxLayout()
        lay.addWidget(leftWidget)
        lay.addWidget(self.__rightWidget)
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

    def setOnlyFindTextWidget(self, f: bool):
        if self.__findTextWidget.isVisible():
            pass
        else:
            if f:
                self.__findTextWidget.setVisible(f)
            else:
                self.__findTextWidget.setVisible(not f)
        self.__findTextWidget.setCloseBtn(f)
        self.__replaceTextWidget.setVisible(not f)
        self.__rightWidget.setVisible(not f)

    def close(self):
        self.__findTextWidget.close()
        super().close()