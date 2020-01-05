import sys
from PySide2.QtWidgets import QApplication
from classes import CurrencyConverter

if __name__ == '__main__':
    app = QApplication(sys.argv)
    currencyConverter = CurrencyConverter()
    currencyConverter.show()
    sys.exit(app.exec_())