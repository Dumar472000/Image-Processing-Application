# ================================== All Libraries ==================================
# ===================================================================================

# ==== PyQt Modules ==== #
# PyQt Widgets
from PyQt5.QtWidgets import QApplication

# Importing Main Application
from gui.app import DigitalImageProcessingApp

# Other Necessary Libraries
import sys

# ======================================= Main ======================================
# ===================================================================================

def main():
    app = QApplication(sys.argv)
    window = DigitalImageProcessingApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()