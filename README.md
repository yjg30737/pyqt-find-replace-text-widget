# pyqt-find-replace-text-widget

## General Info
PyQt5 Widget to find and replace text in QTextEdit, QTextBrowser

## Class Overview
* FindReplaceTextWidget
* ReplaceTextWidget (This module is supposed to be submodule of FindReplaceTextWidget)

## Requirements
PyQt5 >= 5.8

## Setup
``` pip3 install git+https://github.com/yjg30737/pyqt-find-replace-text-widget.git --upgrade ```

Note: <a href="https://github.com/yjg30737/pyqt-find-text-widget.git">pyqt-find-text-widget</a>(main branch) will be automatically installed too. Because it has to be included.

## Usage

I show you my full code sample. Set up this package, copy and paste this code to your IDE and run.

```python
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget, QTextEdit
from pyqt_find_replace_text_widget.findReplaceTextWidget import FindReplaceTextWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__te = QTextEdit()
        self.__w = FindReplaceTextWidget(self.__te)

        lay = QGridLayout()
        lay.addWidget(self.__w)
        lay.addWidget(self.__te)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
```
