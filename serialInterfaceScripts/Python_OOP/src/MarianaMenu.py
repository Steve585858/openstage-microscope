

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction, QFileDialog, QDesktopWidget, QMessageBox, QSizePolicy, QToolBar, QStatusBar, QDockWidget, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from actions_file import FileActions, TestAction
from actions_edit import EditActions
from actions_operation import OperationActions

class MarianaMenu():

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def createMenu(self, menu_bar):
        menu_bar.setNativeMenuBar(False)

        # Create file menu and add actions 
        file_menu = menu_bar.addMenu('File')
        self.fileOpen = FileActions(self.parent, "Open")
        file_menu.addAction(self.fileOpen)
        self.fileSave = FileActions(self.parent, "Save")
        file_menu.addAction(self.fileSave)
        file_menu.addSeparator()
        self.filePrint = FileActions(self.parent, "Print")
        file_menu.addAction(self.filePrint)
        file_menu.addSeparator()
        self.fileExit = FileActions(self.parent, "Exit")
        file_menu.addAction(self.fileExit)

        edit_menu = menu_bar.addMenu('Edit')
        self.editRotate90 = EditActions(self.parent, "Rotate 90")
        edit_menu.addAction(self.editRotate90)
        self.editRotate180 = EditActions(self.parent, "Rotate 180")
        edit_menu.addAction(self.editRotate180)

        # Create edit menu and add actions 
        # edit_menu = menu_bar.addMenu('Edit')
        # edit_menu.addAction(maActions.rotate90_act)
        # edit_menu.addAction(maActions.rotate180_act)
        # edit_menu.addSeparator()
        # edit_menu.addAction(maActions.flip_hor_act)
        # edit_menu.addAction(maActions.flip_ver_act)
        # edit_menu.addSeparator()
        # edit_menu.addAction(maActions.resize_act)
        # edit_menu.addSeparator()
        # edit_menu.addAction(maActions.clear_act)

        # Create view menu and add actions 
        # view_menu = menu_bar.addMenu('View')
        # view_menu.addAction(TestAction(self.parent))
        #view_menu.addAction(maActions.toggle_dock_tools_act)

        #Operation
        operation_menu = menu_bar.addMenu('Operation')
        self.opScan = OperationActions(self.parent, "Scan")
        operation_menu.addAction(self.opScan)
        operation_menu.addSeparator()
        self.opMoveLeft = OperationActions(self.parent, "Move Left")
        operation_menu.addAction(self.opMoveLeft)
        self.opMoveRight = OperationActions(self.parent, "Move Right")
        operation_menu.addAction(self.opMoveRight)



    