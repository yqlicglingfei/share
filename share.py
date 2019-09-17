import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import numpy as np
import pandas as pd
import tushare as ts
import threading as th
import matplotlib.pyplot as plt

class Share(QWidget):
    def __init__(self, parent=None):
        super(Share, self).__init__(parent)
        self.initUI()
        timer = th.Timer(1, self.funTimer)
        timer.start()
        
    def initUI(self):
        loadUi('share.ui', self)
        df = ts.get_stock_basics()
        stocks = df.index.tolist()
        self.codeComboBox.addItems(stocks)
        self.codeComboBox.setEditable(True)
        #self.inputEdit.isClearButtonEnabled(True)
        self.inputEdit.setInputMask('000000;*')
        self.inputEdit.setText(self.codeComboBox.currentText())
        self.inputEdit.textChanged.connect(self.onEditFinish)
        #self.addBtn.setEnabled(False)
        self.addBtn.clicked.connect(self.onAddBtnClick)
        self.delBtn.clicked.connect(self.onDelBtnClick)
        self.codeComboBox.currentIndexChanged.connect(self.onCurrentIndexChanged)
        self.codeComboBox.currentTextChanged.connect(self.onCurrentTextChanged)
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)
        #self.tableWidget.horizontalHeader().setVisible(False)
        #self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("50ETF"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("510050"))
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)
        self.tableWidget.setItem(1, 0, QTableWidgetItem("zhongzheng500"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("512500"))
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)
        self.tableWidget.setItem(2, 0, QTableWidgetItem("shen100"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("159901"))
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)
        self.tableWidget.setItem(3, 0, QTableWidgetItem("kejiETF"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("515000"))
        #rowCount = self.tableWidget.rowCount()
        #self.tableWidget.insertRow(rowCount)
        self.setFixedSize(self.size())

    def funTimer(self):
        global timer
        self.loadValue()
        timer = th.Timer(1, self.funTimer)
        timer.start()
    
    def loadValue(self):
        codes = [self.tableWidget.item(i, 1).text() for i in range(self.tableWidget.rowCount())]
        i = 0
        for code in codes:
            df = ts.get_realtime_quotes(code)
            name = df['name'][0]
            value = df['price'][0]
            maxValue = df['high'][0]
            minValue = df['low'][0]
            volValue = df['volume'][0]
            self.tableWidget.setItem(i, 0, QTableWidgetItem(name))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(code))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(value))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(maxValue))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(minValue))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(volValue))
            i += 1
        
    def findItem(self, value):
        if self.codeComboBox.findText(value) == -1:
            return False
        else:
            return True

    def onAddBtnClick(self):
        value = self.inputEdit.text()
        if self.findItem(value):
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCount)
            self.tableWidget.setItem(rowCount, 1, QTableWidgetItem(value))
        
    def onDelBtnClick(self):
        row = self.tableWidget.currentRow()
        self.tableWidget.removeRow(row)

    def onEditFinish(self):
        value = self.inputEdit.text()
        index = self.codeComboBox.findText(value)
        if index != -1:
            self.codeComboBox.setCurrentIndex(index)
            self.addBtn.setEnabled(True)
        else:
            self.addBtn.setEnabled(False)

    def onCurrentIndexChanged(self, index):
        value = self.codeComboBox.itemText(index)
        self.inputEdit.setText(value)

    def onCurrentTextChanged(self, str):
        self.inputEdit.setText(str)
        
app = QApplication(sys.argv)
w = Share()
w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
w.show()
sys.exit(app.exec())
