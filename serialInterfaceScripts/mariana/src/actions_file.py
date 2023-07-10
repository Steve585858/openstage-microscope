from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction, QFileDialog, QDesktopWidget, QMessageBox, QSizePolicy, QToolBar, QStatusBar, QDockWidget, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from dialogs_settings import dialogsSettings


class FileActions(QAction):
    def __init__(self, parent, actionName):
        #super(OpenFileAction, self).__init__("Open", parent)
        self.parent = parent
        self.actionName = actionName
        super().__init__("", parent)
        self.triggered.connect(self.handle_action)

        self.setText(actionName)
        if(self.actionName=="Open"):
            self.setIcon(QIcon('images/open_file.png'))
            self.setShortcut('Ctrl+O')
            self.setStatusTip('Open a new image')
        elif(self.actionName=="Save"):
            self.setIcon(QIcon('images/save_file.png'))
            self.setShortcut('Ctrl+S')
            self.setStatusTip('Save image')
        elif(self.actionName=="Print"):
            self.setIcon(QIcon('images/print.png'))
            self.setShortcut('Ctrl+P')
            self.setStatusTip('Print image')
        elif(self.actionName=="Settings"):
            self.setShortcut('Ctrl+1')
            self.setStatusTip('Edit Settings')
        elif(self.actionName=="Exit"):
            self.setIcon(QIcon('images/exit.png'))
            self.setShortcut('Ctrl+Q')
            self.setStatusTip('Quit program')
    

    def handle_action(self):
        if(self.actionName=="Open"):
            self.openImage(self.parent)
        elif(self.actionName=="Save"):
            self.saveImage(self.parent)
        elif(self.actionName=="Print"):
            self.printImage(self.parent)
        elif(self.actionName=="Settings"):
            self.editSettings(self.parent)
        elif(self.actionName=="Exit"):
            self.close(self.parent)
        
    def close(self, parent):
        parent.close()

    def openImage(self, parent):
        """
        Open an image file and display its contents in label widget.
        Display error message if image can't be opened. 
        """
        image_file, _ = QFileDialog.getOpenFileName(parent, "Open Image",
            "", "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;Bitmap Files (*.bmp);;\
                GIF Files (*.gif)")

        if image_file:
            parent.image = QPixmap(image_file)

            parent.image_label.setPixmap(parent.image.scaled(parent.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            QMessageBox.information(parent, "Error", 
                "Unable to open image.", QMessageBox.Ok)

        #self.print_act.setEnabled(True)
    
    def saveImage(self, parent):
        """
        Save the image.
        Display error message if image can't be saved. 
        """
        image_file, _ = QFileDialog.getSaveFileName(parent, "Save Image",
            "", "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;Bitmap Files (*.bmp);;\
                GIF Files (*.gif)")

        if image_file and parent.image.isNull() == False:
            parent.image.save(image_file)
        else:
            QMessageBox.information(parent, "Error", 
                "Unable to save image.", QMessageBox.Ok)

    def printImage(self, parent):
        """
        Print image.
        """
        # create printer object and print output defined by the platform
        # the program is being run on. 
        # QPrinter.NativeFormat is the default
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.NativeFormat) 

        # Create printer dialog to configure printer
        print_dialog = QPrintDialog(printer)
        
        # if the dialog is accepted by the user, begin printing
        if (print_dialog.exec_() == QPrintDialog.Accepted):
            # use QPainter to output a PDF file 
            painter = QPainter()
            # begin painting device
            painter.begin(printer)
            # Set QRect to hold painter's current viewport, which 
            # is the image_label 
            rect = QRect(painter.viewport())
            # get the size of image_label and use it to set the size 
            # of the viewport
            size = QSize(parent.image_label.pixmap().size())
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(parent.image_label.pixmap().rect())
            # scale the image_label to fit the rect source (0, 0) 
            painter.drawPixmap(0, 0, parent.image_label.pixmap())
            # end painting
            painter.end()
    
    def editSettings(self, parent):
        print("Control LED")
        dialog = dialogsSettings(parent, "Edit Settings")
        dialog.setFixedSize(500, 700)
        dialog.show()

class TestAction(QAction):
    def __init__(self, parent):
        super(TestAction, self).__init__("Test", parent)
        self.triggered.connect(self.open_file)

    def open_file(self):
        # Implement the logic to open a file here
        print("Open File action triggered")