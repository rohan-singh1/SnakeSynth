# This Python file uses the following encoding: utf-8


# Import the sys module, which provides access to some variables used or maintained by the Python interpreter
import sys

# Import the MainWidget class from the form module
# This module is defining a graphical user interface (GUI) form or widget that the program will display
from form import MainWidget

# Import the QApplication class from the PySide6.QtWidgets module
# This class is used to create a GUI application with a main event loop that listens for events from the operating system or user
# You can install PySide6 with: pip install PySide6
from PySide6.QtWidgets import QApplication

# Check if this module is being run as the main program
if __name__ == "__main__":
    # Create an instance of the QApplication class with no arguments
    app = QApplication([])
    
    # Create an instance of the MainWidget class and assign it to the widget variable
    widget = MainWidget()
    
    # Show the widget on the screen
    widget.show()
    
    # Run the application's event loop and exit the program with the same exit code
    # This function call is necessary to ensure proper cleanup of the GUI application and its resources
    sys.exit(app.exec())