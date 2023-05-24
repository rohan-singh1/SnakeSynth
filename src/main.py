# This Python file uses the following encoding: utf-8

import sys
from form import MainWidget
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSize

WINDOW_WIDTH = 776
WINDOW_HEIGHT = 444

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWidget()
    widget.setWindowTitle("Snake Synth")
    widget.setFixedSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
    widget.show()
    sys.exit(app.exec())
