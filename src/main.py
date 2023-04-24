# This Python file uses the following encoding: utf-8

import sys
from form import MainWidget
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec())
