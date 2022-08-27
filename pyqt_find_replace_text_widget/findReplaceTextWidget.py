from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from pyqt_find_text_widget.findTextWidget import FindTextWidget

from pyqt_find_replace_text_widget.replaceTextWidget import ReplaceTextWidget
from pyqt_svg_button import SvgButton


class FindReplaceTextWidget(QWidget):
    closeSignal = pyqtSignal()

    def __init__(self, widget):
        super().__init__()
        self.__widget = widget
        self.__initUi()

    def __initUi(self):
        self.__findTextWidget = FindTextWidget(self.__widget)
        self.__findTextWidget.closeSignal.connect(self.close)

        self.__replaceTextWidget = ReplaceTextWidget(self.__widget)
        self.__replaceTextWidget.replaceSignal.connect(self.__findTextWidget.next)

        self.__findTextLineEdit = self.__findTextWidget.getLineEdit()
        self.__findTextLineEdit.textChanged.connect(self.__prepareToReplaceFoundText)
        self.setFocusProxy(self.__findTextLineEdit)

        self.__replaceTextLineEdit = self.__replaceTextWidget.getLineEdit()

        self.__widget.textChanged.connect(self.__findTextWidget.widgetTextChanged)

        lay = QVBoxLayout()
        lay.addWidget(self.__findTextWidget)
        lay.addWidget(self.__replaceTextWidget)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(2)

        standardTextWidgetHeight = max(self.__findTextWidget.sizeHint().height(),
                                       self.__replaceTextWidget.sizeHint().height())

        self.__findTextWidget.setMinimumHeight(standardTextWidgetHeight)
        self.__replaceTextWidget.setMinimumHeight(standardTextWidgetHeight)

        self.__findTextLineEdit.setStyleSheet('QLineEdit { border: 1px solid gray; }')
        self.__replaceTextLineEdit.setStyleSheet('QLineEdit { border: 1px solid gray; }')

        standardLineEditWidth = 100
        standardLineEditHeight = standardTextWidgetHeight

        self.__findTextLineEdit.setMinimumHeight(standardLineEditHeight)
        self.__replaceTextLineEdit.setMinimumHeight(standardLineEditHeight)

        self.__findTextLineEdit.setMinimumWidth(standardLineEditWidth)
        self.__replaceTextLineEdit.setMinimumWidth(standardLineEditWidth)

        leftWidget = QWidget()
        leftWidget.setLayout(lay)

        swapBtn = SvgButton()
        swapBtn.clicked.connect(self.__swap)
        swapBtn.setIcon('ico/swap_v.svg')

        closeBtn = SvgButton()
        closeBtn.setShortcut('Escape')
        closeBtn.clicked.connect(self.close)
        closeBtn.setIcon('ico/close.svg')

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

        self.setTabOrder(self.__findTextLineEdit, self.__replaceTextLineEdit)

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
        super().close()
        self.closeSignal.emit()

    def resizeEvent(self, e):
        return super().resizeEvent(e)