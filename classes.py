from currency_converter import RateNotFoundError, CurrencyConverter as CurrencyConverter_
from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QLineEdit, QPushButton, QHBoxLayout, QComboBox

def parseToFloat(value, valueOnError = None):
    try:
        return round(float(value), 2)
    except ValueError:
        return valueOnError

class CurrencyConverter(QDialog):
    c = CurrencyConverter_()
    config = {
      'title': 'Convertisseur de devises',
      'bgColor': '#333',
      'uiColor': '#FFFFFF',
      'uiMaxWidth': 150,
      'width': 800,
      'height': 220,
    }
    currencies = []
    buttonInverter = None
    currentCurrency = {
      'amount': 1,
      'code': 'EUR',
      'input': None,
      'select': None,
    }
    targetCurrency = {
      'amount': None,
      'code': 'USD',
      'input': None,
      'select': None,
    }

    def __init__(self, parent = None):
        super(CurrencyConverter, self).__init__(parent)
        self.setWindowTitle(self.config['title'])
        self.setStyleSheet(''.join(['background-color:', self.config['bgColor'], ';']))
        self.setMinimumSize(self.config['width'], self.config['height'])
        self.initCurrencies()
        self.addForm()

    def addForm(self):
        layout = QHBoxLayout()
        '''
        Instanciation des UI
        '''
        self.currentCurrency['input'] = QLineEdit()
        self.currentCurrency['select'] = QComboBox()
        self.targetCurrency['input'] = QLineEdit()
        self.targetCurrency['select'] = QComboBox()
        self.buttonInverter = QPushButton('Inverser devises')

        '''
        Modification du style
        '''
        self.currentCurrency['input'].setFixedWidth(self.config['uiMaxWidth'])
        self.currentCurrency['select'].setFixedWidth(self.config['uiMaxWidth'])
        self.targetCurrency['input'].setFixedWidth(self.config['uiMaxWidth'])
        self.targetCurrency['select'].setFixedWidth(self.config['uiMaxWidth'])
        self.buttonInverter.setFixedWidth(self.config['uiMaxWidth'])

        colorStyle = ''.join(['color:', self.config['uiColor'], ';'])
        self.currentCurrency['input'].setStyleSheet(colorStyle)
        self.currentCurrency['select'].setStyleSheet(colorStyle)
        self.targetCurrency['input'].setStyleSheet(colorStyle)
        self.targetCurrency['select'].setStyleSheet(colorStyle)
        self.buttonInverter.setStyleSheet(colorStyle)

        '''
        Ajout des données
        '''
        self.currentCurrency['select'].addItems(self.currencies)
        self.targetCurrency['select'].addItems(self.currencies)
        self.initDefaultCurrency(self.currentCurrency['select'], self.currentCurrency['code'])
        self.initDefaultCurrency(self.targetCurrency['select'], self.targetCurrency['code'])
        self.currentCurrency['input'].setText(str(self.currentCurrency['amount']))
        self.initDefaultValues()

        '''
        Ajout des évènements
        '''
        self.currentCurrency['select'].currentIndexChanged.connect(self.onCurrentCurrencyChange)
        self.targetCurrency['select'].currentIndexChanged.connect(self.onTargetCurrencyChange)
        self.currentCurrency['input'].textChanged.connect(self.onCurrentAmountChange)
        self.targetCurrency['input'].textChanged.connect(self.onTargetAmountChange)
        self.buttonInverter.clicked.connect(self.onClickInverter)

        '''
        Ajout des éléments à l'interface
        '''
        layout.addWidget(self.currentCurrency['select'])
        layout.addWidget(self.currentCurrency['input'])
        layout.addWidget(self.targetCurrency['select'])
        layout.addWidget(self.targetCurrency['input'])
        layout.addWidget(self.buttonInverter)
        self.setLayout(layout)

    def initCurrencies(self):
        self.currencies = sorted(self.c.currencies)

    def initDefaultCurrency(self, selec, code):
        index = selec.findText(code, QtCore.Qt.MatchFixedString)
        if index >= 0:
            selec.setCurrentIndex(index)

    def convert(self, amount, currentDevice, targetDevice):
      result = None
      try:
        result = self.c.convert(amount, currentDevice, targetDevice)
      except RateNotFoundError:
        '''
        impossible de convertir xx device vers xx device, cela n'est pas prit en compte pour l'instant.
        '''
      return result

    def onInputChange(self, action, force = False):
        currency1 = self.currentCurrency['select'].currentText()
        currency2 = self.targetCurrency['select'].currentText()
        amount1 = self.currentCurrency['input'].text()
        amount2 = self.targetCurrency['input'].text()
        amount1 = parseToFloat(amount1, -1)
        amount2 = parseToFloat(amount2, -1)

        if action == 'INVERTER':
            self.initDefaultCurrency(self.currentCurrency['select'], currency2)
            self.initDefaultCurrency(self.targetCurrency['select'], currency1)
            self.currentCurrency['input'].setText(str(amount2))
            self.targetCurrency['input'].setText(str(amount1))

        if action == 'UPDATE_TARGET_AMOUNT' and (force or amount1 != parseToFloat(self.currentCurrency['amount'])):
            if amount1 < 0:
              self.targetCurrency['input'].setText(str(''))
              return

            nextValue = parseToFloat(self.convert(amount1, currency1, currency2))
            self.currentCurrency['amount'] = amount1
            self.targetCurrency['amount'] = nextValue
            self.targetCurrency['input'].setText(str(nextValue))

        if action == 'UPDATE_CURRENT_AMOUNT' and (force or amount2 != parseToFloat(self.targetCurrency['amount'])):
            if amount2 < 0:
              self.currentCurrency['input'].setText(str(''))
              return

            nextValue = parseToFloat(self.convert(amount2, currency2, currency1))
            self.targetCurrency['amount'] = amount2
            self.currentCurrency['amount'] = nextValue
            self.currentCurrency['input'].setText(str(nextValue))

    def initDefaultValues(self):
        self.onInputChange('UPDATE_TARGET_AMOUNT', True)

    def onCurrentAmountChange(self):
        self.onInputChange('UPDATE_TARGET_AMOUNT')

    def onTargetAmountChange(self):
        self.onInputChange('UPDATE_CURRENT_AMOUNT')

    def onCurrentCurrencyChange(self):
        self.onInputChange('UPDATE_TARGET_AMOUNT', True)

    def onTargetCurrencyChange(self):
        self.onInputChange('UPDATE_CURRENT_AMOUNT', True)

    def onClickInverter(self):
        self.onInputChange('INVERTER')