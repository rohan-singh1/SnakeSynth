# This Python file uses the following encoding: utf-8

import sys
from form import MainWidget
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSize

window_width = 610
window_height = 310


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWidget()
    widget.setFixedSize(QSize(window_width, window_height))
    widget.show()
    sys.exit(app.exec())
