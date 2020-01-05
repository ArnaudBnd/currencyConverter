from currency_converter import RateNotFoundError, CurrencyConverter as CurrencyConverter_
from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QLineEdit, QPushButton, QHBoxLayout, QComboBox, QMessageBox

    '''
    Parse value to float to display
    '''
def parseFloat(value, valueOnError = None):
    try:
        return round(float(value), 3)
    except ValueError:
        return valueOnError

class CurrencyConverter(QDialog):
    c = CurrencyConverter_()
    currencies = []
    currentCurrency = {
      'amount': 1,
      'code': 'EUR',
      'input': None,
      'select': None,
      'update': 'currentUpdated'
    }
    targetCurrency = {
      'amount': None,
      'code': 'USD',
      'input': None,
      'select': None,
      'update': 'targetUpdated',
    }

    '''
    Initializer
    '''
    def __init__(self, parent = None):
        super(CurrencyConverter, self).__init__(parent)
        self.currencies = sorted(self.c.currencies)
        self.createInterface()

    def onCurrentAmountChange(self):
        self.changeInput(self.targetCurrency['update'])

    def onTargetAmountChange(self):
        self.changeInput(self.currentCurrency['update'])

    def onCurrentCurrencyChange(self):
        self.changeInput(self.targetCurrency['update'], True, True)

    def onTargetCurrencyChange(self):
        self.changeInput(self.currentCurrency['update'], True)

    def initDefaultCurrency(self, selec, code):
        index = selec.findText(code, QtCore.Qt.MatchFixedString)
        if index >= 0:
            selec.setCurrentIndex(index)

    '''
    Button to reverse the converters
    '''
    def onClick(self):
        #Get currency selected
        currency1 = self.currentCurrency['select'].currentText()
        currency2 = self.targetCurrency['select'].currentText()
        #Get amount selected
        amount1 = self.currentCurrency['input'].text()
        amount2 = self.targetCurrency['input'].text()

        self.initDefaultCurrency(self.currentCurrency['select'], currency2)
        self.initDefaultCurrency(self.targetCurrency['select'], currency1)
        self.currentCurrency['input'].setText(str(parseFloat(amount2, -1)))
        self.targetCurrency['input'].setText(str(parseFloat(amount1, -1)))

    '''
    Interface creation
    '''
    def createInterface(self):
        layout = QHBoxLayout()
        buttonToInvert = None

        '''
        Adding title
        '''
        self.setWindowTitle('Convertisseur de devises')

        '''
        Adding style of window
        '''
        self.setStyleSheet(''.join(['background-color:', '#333', ';']))

        '''
        Adding width and height
        '''
        self.setMinimumSize(800, 250)

        '''
        Adding UI
        '''
        self.buttonToInvert = QPushButton('Inverser devises')
        self.currentCurrency['input'] = QLineEdit()
        self.currentCurrency['select'] = QComboBox()
        self.targetCurrency['input'] = QLineEdit()
        self.targetCurrency['select'] = QComboBox()

        '''
        Adding datas
        '''
        self.currentCurrency['select'].addItems(self.currencies)
        self.targetCurrency['select'].addItems(self.currencies)
        self.initDefaultCurrency(self.currentCurrency['select'], self.currentCurrency['code'])
        self.initDefaultCurrency(self.targetCurrency['select'], self.targetCurrency['code'])
        self.currentCurrency['input'].setText(str(1))
        self.changeInput(self.targetCurrency['update'], True)

        '''
        Adding style
        '''
        self.currentCurrency['input'].setFixedWidth(150)
        self.currentCurrency['select'].setFixedWidth(150)
        self.targetCurrency['input'].setFixedWidth(150)
        self.targetCurrency['select'].setFixedWidth(150)
        self.buttonToInvert.setFixedWidth(150)
        self.currentCurrency['input'].setStyleSheet(''.join(['color:', '#FFFFFF', ';']))
        self.currentCurrency['select'].setStyleSheet(''.join(['color:', '#FFFFFF', ';']))
        self.targetCurrency['input'].setStyleSheet(''.join(['color:', '#FFFFFF', ';']))
        self.targetCurrency['select'].setStyleSheet(''.join(['color:', '#FFFFFF', ';']))
        self.buttonToInvert.setStyleSheet(''.join(['color:', '#FFFFFF', ';']))

        '''
        Adding events
        '''
        self.currentCurrency['select'].currentIndexChanged.connect(self.onCurrentCurrencyChange)
        self.targetCurrency['select'].currentIndexChanged.connect(self.onTargetCurrencyChange)
        self.currentCurrency['input'].textChanged.connect(self.onCurrentAmountChange)
        self.targetCurrency['input'].textChanged.connect(self.onTargetAmountChange)
        self.buttonToInvert.clicked.connect(self.onClick)

        '''
        Adding elements to the interface
        '''
        layout.addWidget(self.currentCurrency['select'])
        layout.addWidget(self.currentCurrency['input'])
        layout.addWidget(self.targetCurrency['select'])
        layout.addWidget(self.targetCurrency['input'])
        layout.addWidget(self.buttonToInvert)
        self.setLayout(layout)

    '''
    During changes
    '''
    def changeInput(self, action, force = False, changeCurrent = False):
        #Get currency selected
        currency1 = self.currentCurrency['select'].currentText()
        currency2 = self.targetCurrency['select'].currentText()
        #Get amount selected
        amount1 = self.currentCurrency['input'].text()
        amount2 = self.targetCurrency['input'].text()

        if amount1 == "":
            self.targetCurrency['input'].setText(str(''))

        if action == 'targetUpdated' and (force or parseFloat(amount1, -1) != parseFloat(1) and amount1 != ""):
            #Display pop-up error
            if (parseFloat(amount1, -1) < 0) and changeCurrent != True:
              QMessageBox.about(self, "Title", "Enter a valid value please")
              self.targetCurrency['input'].setText(str(''))
              self.currentCurrency['input'].setText(str(''))
              return

            nextValue = parseFloat(self.c.convert(parseFloat(amount1, -1), currency1, currency2))
            self.currentCurrency['amount'] = parseFloat(amount1, -1)
            self.targetCurrency['amount'] = nextValue
            self.targetCurrency['input'].setText(str(nextValue))

        if action == 'currentUpdated' and (force or parseFloat(amount2, -1) != parseFloat(self.targetCurrency['amount'])):
            if parseFloat(amount2, -1) < 0:
              self.currentCurrency['input'].setText(str(''))
              return

            nextValue = parseFloat(self.c.convert(parseFloat(amount2, -1), currency2, currency1))
            self.targetCurrency['amount'] = parseFloat(amount2, -1)
            self.currentCurrency['amount'] = nextValue
            self.currentCurrency['input'].setText(str(nextValue))