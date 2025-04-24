"""
Main entry point for the Go game application.
Launches the graphical user interface by default.
"""

import sys
from PySide6.QtWidgets import QApplication
from menus.go.go_gui import GoGameGUI

def main():
    #Launch the Go game graphical user interface"
    app = QApplication(sys.argv)
    window = GoGameGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()