

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction, QFileDialog, QDesktopWidget, QMessageBox, QSizePolicy, QToolBar, QStatusBar, QDockWidget, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

class MaMenu():

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def createMenu(self, maActions, menu_bar):
        menu_bar.setNativeMenuBar(False)

        # Create file menu and add actions 
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(maActions.open_act)
        file_menu.addAction(maActions.save_act)
        file_menu.addSeparator()
        file_menu.addAction(maActions.print_act)
        file_menu.addSeparator()
        file_menu.addAction(maActions.exit_act)

        # Create edit menu and add actions 
        edit_menu = menu_bar.addMenu('Edit')
        edit_menu.addAction(maActions.rotate90_act)
        edit_menu.addAction(maActions.rotate180_act)
        edit_menu.addSeparator()
        edit_menu.addAction(maActions.flip_hor_act)
        edit_menu.addAction(maActions.flip_ver_act)
        edit_menu.addSeparator()
        edit_menu.addAction(maActions.resize_act)
        edit_menu.addSeparator()
        edit_menu.addAction(maActions.clear_act)

        # Create view menu and add actions 
        view_menu = menu_bar.addMenu('View')
        #view_menu.addAction(maActions.toggle_dock_tools_act)

    