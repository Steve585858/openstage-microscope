import sys, os
import configparser
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QWidget, QDialog, QDialogButtonBox, QTextEdit, QGridLayout
from PyQt5.QtCore import Qt

class dialogsSettings(QDialog):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle(title)
        
        
        
        mainGridLayout = QGridLayout(self)
        
        label = QLabel("Edit Settings")
        label.setAlignment(Qt.AlignHCenter)
        font = label.font()
        font.setBold(True)
        iRow = 0
        iCol = 0
        rowSpan = 1
        colSpan = 2
        mainGridLayout.addWidget(label, iRow, iCol, rowSpan, colSpan)
        colSpan = 1
        
        parser = configparser.ConfigParser()
        parser.read(os.path.join(self.parent.path_root, 'config.ini'))
        for section in parser.sections():
            for key,value in parser.items(section):
                iRow += 1
                label = QLabel(self)
                label.setText(key)
                line_edit = QLineEdit(self)
                line_edit.setText(value)
                iCol = 0
                mainGridLayout.addWidget(label, iRow, iCol, rowSpan, colSpan)
                iCol += 1
                mainGridLayout.addWidget(line_edit, iRow, iCol, rowSpan, colSpan)
        
        buttonBox = QDialogButtonBox()
        buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        ok_button = buttonBox.button(QDialogButtonBox.Ok)
        ok_button.setText("Update Information")
        
        iRow += 1
        iCol = 0
        colSpan = 2
        mainGridLayout.addWidget(buttonBox, iRow, iCol, rowSpan, colSpan)
        
        self.setLayout(mainGridLayout)
        
    def buttonPressed(self):
        pass