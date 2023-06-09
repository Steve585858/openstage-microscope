

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction, QFileDialog, QDesktopWidget, QMessageBox, QSizePolicy, QToolBar, QStatusBar, QDockWidget, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

class MaActions():

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.createActions(self.parent)

    def createActions(self, parent):
        # Create actions for file menu
        self.open_act = QAction(QIcon('images/open_file.png'),"Open", parent)
        self.open_act.setShortcut('Ctrl+O')
        self.open_act.setStatusTip('Open a new image')
        self.open_act.triggered.connect(self.openImage)

        self.save_act = QAction(QIcon('images/save_file.png'),"Save", parent)
        self.save_act.setShortcut('Ctrl+S')
        self.save_act.setStatusTip('Save image')
        self.save_act.triggered.connect(self.saveImage)

        self.print_act = QAction(QIcon('images/print.png'), "Print", parent)
        self.print_act.setShortcut('Ctrl+P')
        self.print_act.setStatusTip('Print image')
        self.print_act.triggered.connect(self.printImage)
        self.print_act.setEnabled(False)

        self.exit_act = QAction(QIcon('images/exit.png'), 'Exit', parent)
        self.exit_act.setShortcut('Ctrl+Q')
        self.exit_act.setStatusTip('Quit program')
        self.exit_act.triggered.connect(parent.close)

        # Create actions for edit menu
        self.rotate90_act = QAction("Rotate 90º", parent)
        self.rotate90_act.setStatusTip('Rotate image 90º clockwise')
        self.rotate90_act.triggered.connect(self.rotateImage90)

        self.rotate180_act = QAction("Rotate 180º", parent)
        self.rotate180_act.setStatusTip('Rotate image 180º clockwise')
        self.rotate180_act.triggered.connect(self.rotateImage180)

        self.flip_hor_act = QAction("Flip Horizontal", parent)
        self.flip_hor_act.setStatusTip('Flip image across horizontal axis')
        self.flip_hor_act.triggered.connect(self.flipImageHorizontal)

        self.flip_ver_act = QAction("Flip Vertical", parent)
        self.flip_ver_act.setStatusTip('Flip image across vertical axis')
        self.flip_ver_act.triggered.connect(self.flipImageVertical)

        self.resize_act = QAction("Resize Half", parent)
        self.resize_act.setStatusTip('Resize image to half the original size')
        self.resize_act.triggered.connect(self.resizeImageHalf)

        self.clear_act = QAction(QIcon('images/clear.png'), "Clear Image", parent)
        self.clear_act.setShortcut("Ctrl+D")
        self.clear_act.setStatusTip('Clear the current image')
        self.clear_act.triggered.connect(self.clearImage)

    def openImage(self):
        """
        Open an image file and display its contents in label widget.
        Display error message if image can't be opened. 
        """
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image",
            "", "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;Bitmap Files (*.bmp);;\
                GIF Files (*.gif)")

        if image_file:
            self.image = QPixmap(image_file)

            self.image_label.setPixmap(self.image.scaled(self.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            QMessageBox.information(self, "Error", 
                "Unable to open image.", QMessageBox.Ok)

        self.print_act.setEnabled(True)

    def saveImage(self):
        """
        Save the image.
        Display error message if image can't be saved. 
        """
        image_file, _ = QFileDialog.getSaveFileName(self, "Save Image",
            "", "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;Bitmap Files (*.bmp);;\
                GIF Files (*.gif)")

        if image_file and self.image.isNull() == False:
            self.image.save(image_file)
        else:
            QMessageBox.information(self, "Error", 
                "Unable to save image.", QMessageBox.Ok)

    def printImage(self):
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
            size = QSize(self.image_label.pixmap().size())
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.image_label.pixmap().rect())
            # scale the image_label to fit the rect source (0, 0) 
            painter.drawPixmap(0, 0, self.image_label.pixmap())
            # end painting
            painter.end()
            
    def clearImage(self):
        """
        Clears current image in QLabel widget
        """
        self.image_label.clear()
        self.image = QPixmap() # reset pixmap so that isNull() = True

    def rotateImage90(self):
        """
        Rotate image 90º clockwise
        """
        if self.image.isNull() == False:
            transform90 = QTransform().rotate(90)
            pixmap = QPixmap(self.image)

            rotated = pixmap.transformed(transform90, mode=Qt.SmoothTransformation)

            self.image_label.setPixmap(rotated.scaled(self.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QPixmap(rotated) 
            self.image_label.repaint() # repaint the child widget
        else:
            # No image to rotate
            pass

    def rotateImage180(self):
        """
        Rotate image 180º clockwise
        """
        if self.image.isNull() == False:
            transform180 = QTransform().rotate(180)
            pixmap = QPixmap(self.image)

            rotated = pixmap.transformed(transform180, mode=Qt.SmoothTransformation)

            self.image_label.setPixmap(rotated.scaled(self.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
            # .......... To keep being allowed to rotate the image
            self.image = QPixmap(rotated) 
            self.image_label.repaint() # repaint the child widget
        else:
            # No image to rotate
            pass

    def flipImageHorizontal(self):
        """
        Mirror the image across the horizontal axis
        """
        if self.image.isNull() == False:
            flip_h = QTransform().scale(-1, 1)
            pixmap = QPixmap(self.image)

            flipped = pixmap.transformed(flip_h)

            self.image_label.setPixmap(flipped.scaled(self.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QPixmap(flipped)
            self.image_label.repaint()
        else:
            # No image to flip
            pass

    def flipImageVertical(self):
        """
        Mirror the image across the vertical axis
        """
        if self.image.isNull() == False:
            flip_v = QTransform().scale(1, -1)
            pixmap = QPixmap(self.image)

            flipped = pixmap.transformed(flip_v)

            self.image_label.setPixmap(flipped.scaled(self.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QPixmap(flipped)
            self.image_label.repaint()
        else:
            # No image to flip
            pass

    def resizeImageHalf(self):
        """
        Resize the image to half its current size.
        """
        if self.image.isNull() == False:
            resize = QTransform().scale(0.5, 0.5)
            pixmap = QPixmap(self.image)

            resized = pixmap.transformed(resize)

            self.image_label.setPixmap(resized.scaled(self.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QPixmap(resized)
            self.image_label.repaint()
        else:
            # No image to resize
            pass

    