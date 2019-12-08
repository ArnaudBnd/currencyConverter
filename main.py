import sys
from PySide2.QtWidgets import QApplication
from classes import CurrencyConverter

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    currencyConverter = CurrencyConverter()
    currencyConverter.show()
    # Run the main Qt loop
    sys.exit(app.exec_())