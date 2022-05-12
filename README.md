# pyqt-find-replace-text-widget

PyQt widget which can find and replace text in the QTextEdit/QTextBrowser

## Class Overview
* FindReplaceTextWidget
* ReplaceTextWidget (This module is supposed to be submodule of FindReplaceTextWidget)

## Requirements
* PyQt5 >= 5.8

## Setup
`python -m pip install pyqt-find-replace-text-widget`

## Included package
* <a href="https://github.com/yjg30737/pyqt-find-text-widget.git">pyqt-find-text-widget</a>
* <a href="https://github.com/yjg30737/pyqt-resource-helper.git">pyqt-resource-helper</a>

## Example

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
        self.__te.setStyleSheet('QTextEdit { selection-background-color: lightblue; }')

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

Result

Note: Button icons in preview are obsolete.

https://user-images.githubusercontent.com/55078043/146636169-eccd62b4-7964-40c1-a6c6-4fc813778a1e.mp4

## Note
There is exclude button but i don't add feature on it. I will add proper feature on that one.
