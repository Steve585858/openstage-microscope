

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QAction, QFileDialog, QDesktopWidget, QMessageBox, QSizePolicy, QToolBar, QStatusBar, QDockWidget, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

from MaActions import MaActions
from MaMenu import MaMenu

class MaGUI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initializeUI()

    def initializeUI(self):
        #self.setFixedSize(650, 650)
        self.setWindowTitle('MARIANA')
        self.centerMainWindow()
        self.createToolsDockWidget()

        #self.createMenu()
        maActions = MaActions(self)
        menu_bar = self.menuBar()
        maMenu = MaMenu(self)
        maMenu.createMenu(maActions, menu_bar)
        self.setStatusBar(QStatusBar(self))

        #self.createToolBar()
        self.photoEditorWidgets()
        self.show()

    def screen_resolutions(self):
        for displayNr in range(QtWidgets.QDesktopWidget().screenCount()):
            sizeObject = QtWidgets.QDesktopWidget().screenGeometry(displayNr)
            print("Display: " + str(displayNr) + " Screen size : " + str(sizeObject.height()) + "x" + str(sizeObject.width()))


    def createToolBar(self):
        """
        Create toolbar for photo editor GUI
        """
        tool_bar = QToolBar("Photo Editor Toolbar")
        tool_bar.setIconSize(QSize(24,24))
        self.addToolBar(tool_bar)

        # add actions to toolbar
        tool_bar.addAction(self.open_act)
        tool_bar.addAction(self.save_act)
        tool_bar.addAction(self.print_act)
        tool_bar.addAction(self.clear_act)
        tool_bar.addSeparator()
        tool_bar.addAction(self.exit_act)

    def createToolsDockWidget(self):
        """
        Use View -> Edit Image Tools menu and click the dock widget on or off.
        Tools dock can be placed on the left or right of the main window. 
        """
        # set up QDockWidget
        self.dock_tools_view = QDockWidget()
        self.dock_tools_view.setWindowTitle("Edit Image Tools")
        self.dock_tools_view.setAllowedAreas(Qt.LeftDockWidgetArea |
            Qt.RightDockWidgetArea)

        # create container QWidget to hold all widgets inside dock widget
        self.tools_contents = QWidget()

        # create tool push buttons 
        self.rotate90 = QPushButton("Rotate 90º")
        self.rotate90.setMinimumSize(QSize(130, 40))
        self.rotate90.setStatusTip('Rotate image 90º clockwise')
        self.rotate90.clicked.connect(self.rotateImage90)

        self.rotate180 = QPushButton("Rotate 180º")
        self.rotate180.setMinimumSize(QSize(130, 40))
        self.rotate180.setStatusTip('Rotate image 180º clockwise')
        self.rotate180.clicked.connect(self.rotateImage180)

        self.flip_horizontal = QPushButton("Flip Horizontal")
        self.flip_horizontal.setMinimumSize(QSize(130, 40))
        self.flip_horizontal.setStatusTip('Flip image across horizontal axis')
        self.flip_horizontal.clicked.connect(self.flipImageHorizontal)

        self.flip_vertical = QPushButton("Flip Vertical")
        self.flip_vertical.setMinimumSize(QSize(130, 40))
        self.flip_vertical.setStatusTip('Flip image across vertical axis')
        self.flip_vertical.clicked.connect(self.flipImageVertical)

        self.resize_half = QPushButton("Resize Half")
        self.resize_half.setMinimumSize(QSize(130, 40))
        self.resize_half.setStatusTip('Resize image to half the original size')
        self.resize_half.clicked.connect(self.resizeImageHalf)

        # set up vertical layout to contain all the push buttons 
        dock_v_box = QVBoxLayout()
        dock_v_box.addWidget(self.rotate90)
        dock_v_box.addWidget(self.rotate180)
        dock_v_box.addStretch(1)
        dock_v_box.addWidget(self.flip_horizontal)
        dock_v_box.addWidget(self.flip_vertical)
        dock_v_box.addStretch(1)
        dock_v_box.addWidget(self.resize_half)
        dock_v_box.addStretch(6)

        # set the main layout for the QWidget, tools_contents,
        # then set the main widget of the dock widget
        self.tools_contents.setLayout(dock_v_box)
        self.dock_tools_view.setWidget(self.tools_contents)
        
        # set initial location of dock widget
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_tools_view)

        # handles the visibility of the dock widget
        self.toggle_dock_tools_act = self.dock_tools_view.toggleViewAction()

    def photoEditorWidgets(self):
        """
        Set up instances of widgets for photo editor GUI
        """
        self.image = QPixmap()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        # Use setSizePolicy to specify how the widget can be 
        # resized, horizontally and vertically. Here, the image 
        # will stretch horizontally, but not vertically.
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)

        self.setCentralWidget(self.image_label)

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

    def centerMainWindow(self):
        app = QApplication.instance()
        screen = app.screenAt(self.pos())
        geometry = screen.availableGeometry()
        screen_width = geometry.width()
        screen_height = geometry.height()
        self.setFixedSize(int(screen_width * 0.8), int(screen_height * 0.8))
        #desktop = QDesktopWidget().screenGeometry()
        self.move(int((screen_width - self.width()) / 2), int((screen_height - self.height()) / 2))

# Run program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontShowIconsInMenus, True)
    ex = MaGUI()
    sys.exit(app.exec_())
