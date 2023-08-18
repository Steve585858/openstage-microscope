import os
import time
from qasync import asyncSlot

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QFont, QPen
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QWidget, QLabel, QVBoxLayout, QSizePolicy,  \
   QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsEllipseItem, QSpacerItem, QGraphicsLineItem


#Python asyncio event loop in a separate thread
#https://gist.github.com/dmfigol/3e7d5b84a16d076df02baa9f53271058

#This sketch is a server for the telemetrix and telemetrix-aio Python clients.
#https://github.com/MrYsLab/Telemetrix4Arduino
#User Manual https://mryslab.github.io/telemetrix/

#telemetrix-aio API
#https://htmlpreview.github.io/?https://github.com/MrYsLab/telemetrix-aio/blob/master/html/telemetrix_aio/index.html
#source code
#https://github.com/MrYsLab/telemetrix-aio


class MovingObject(QGraphicsEllipseItem):
    def __init__(self, x, y, r):
        super().__init__(0, 0, r, r)
        self.r = r
        self.setPos(x, y)
        self.setBrush(Qt.blue)
        self.setAcceptHoverEvents(True)
        self.statusLabel = None

    # mouse hover event
    def hoverEnterEvent(self, event):
        QApplication.setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        QApplication.restoreOverrideCursor()

    def mousePressEvent(self, event):
        print("mouse pressed")
        #self.testSize(event)

    def isWithinSize(self, x, y):
        views = self.scene().views()
        if views:
            graphics_view = views[0]
            display_size = graphics_view.viewport().size()
            if x>=0 and x<=display_size.width()-self.r and y>=0 and y<=display_size.height()-self.r:
                return True
        
        return False

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        if self.isWithinSize(updated_cursor_x, updated_cursor_y):
            self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
        self.updateMsg()

    def move(self, deltaX, deltaY):
        current_pos = self.pos()
        self.moveTo(current_pos.x()+deltaX, current_pos.y()+deltaY)
    
    def moveTo(self, x, y):
        self.setPos(QPointF(x, y))
        #self.updateMsg()

    def mouseReleaseEvent(self, event):
        self.updateMsg()
    
    def setStatusLabel(self, statusLabel):
        self.statusLabel = statusLabel
    
    def updateMsg(self, msg=None):
        if msg:
            pass
        else: 
            msg = ('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))
        if self.statusLabel:
            self.statusLabel.setText(msg)
        else :
            print(msg)


class MotorControlWidget(QWidget):
    def __init__(self, parent=None, iLayerout=1):
        super().__init__(parent)
        self.parent = parent
        self.board = parent.board
        self.motor_is_running = False
        self.ctrl = {'break': False}
        self.setFocusPolicy(Qt.StrongFocus)

        vBoxLayout = QVBoxLayout(self)

        graphics_view = QGraphicsView()
        graphics_scene = QGraphicsScene()
        graphics_view.setScene(graphics_scene)
        w = 500
        h = 500
        graphics_view.setSceneRect(0, 0, w, h)

        r = 40
        cross_w = w/2
        cross_h = h/2
        r = 40
        self.moveObject = MovingObject(cross_w-r/2, cross_h-r/2, r)
        horizontal_line = self.createQGraphicsLineItem(w/2-cross_w, h/2, w/2+cross_w, h/2)
        graphics_scene.addItem(horizontal_line)
        vertical_line = self.createQGraphicsLineItem(w/2, h/2-cross_h, w/2, h/2+cross_h)
        graphics_scene.addItem(vertical_line)
        graphics_scene.addItem(self.moveObject)
        vBoxLayout.addWidget(graphics_view)
        scene_rect = graphics_view.sceneRect()
        print("Scene size:", scene_rect.width(), "x", scene_rect.height())
 
        widget = QWidget(self)
        gridLayout = QGridLayout(widget)

        iRow = 0
        iCol = 0
        # Insert an empty row
        spacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gridLayout.addItem(spacer, iRow, iCol,1,1)

        iRow += 1
        iCol = 1
        self.toUpBtnY = self.createQPushButton('arrows_up.png', 20)
        gridLayout.addWidget(self.toUpBtnY, iRow, iCol,1,1)

        iCol = 4
        self.toUpBtnZ = self.createQPushButton('arrows_z_up.png', 40)
        gridLayout.addWidget(self.toUpBtnZ, iRow, iCol,1,1)

        iRow += 1
        iCol = 0
        self.toLeftBtnX = self.createQPushButton('arrows_left.png', 1)
        gridLayout.addWidget(self.toLeftBtnX, iRow, iCol,1,1)

        iCol += 1
        #label = QLabel(self)
        #pixmap = QPixmap(os.path.join(self.parent.path_images, 'marianaLogo_greenCircle.png'))
        #scaled_pixmap = pixmap.scaled(60, 60)
        #label.setPixmap(scaled_pixmap)
        label = self.createQLabel("X & Y", QFont('Arial', 12, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        gridLayout.addWidget(label, iRow, iCol,1,1)
        
        iCol += 1
        self.toRightBtnX = self.createQPushButton('arrows_right.png', 10)
        gridLayout.addWidget( self.toRightBtnX, iRow, iCol,1,1)

        iCol += 1
        #spacer = QSpacerItem(5, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)
        #spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Preferred)
        gridLayout.addItem(spacer, iRow, iCol,1,1)

        iCol += 1
        label = self.createQLabel("Z", QFont('Arial', 12, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        gridLayout.addWidget(label, iRow, iCol,1,1)

        iCol = 1
        iRow += 1
        self.toDownBtnY = self.createQPushButton('arrows_down.png', 30)
        gridLayout.addWidget(self.toDownBtnY, iRow, iCol,1,1)

        iCol = 4
        self.toDownBtnZ = self.createQPushButton('arrows_z_down.png', 50)
        gridLayout.addWidget(self.toDownBtnZ, iRow, iCol,1,1)
        
        iRow += 1
        iCol = 0
        # Insert an empty row
        spacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gridLayout.addItem(spacer, iRow, iCol,1,1)

        vBoxLayout.addWidget(widget)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            self.move(30)
        elif event.key() == QtCore.Qt.Key_Down:
            self.move(20)
        elif event.key() == QtCore.Qt.Key_Left:
            self.move(1)
        elif event.key() == QtCore.Qt.Key_Right:
            self.move(10)
        elif event.key() == QtCore.Qt.Key_U:
            self.move(40)
        elif event.key() == QtCore.Qt.Key_D:
            self.move(50)
        else:
            print("no arrow key is pressed")

    def resizeEvent(self, event):
        new_size = event.size()
        #print("Graphic Widget resized to:", new_size)
        
    def createQPushButton(self, iconFileName, actionId, iconSize=QtCore.QSize(50, 30)):
        b = QPushButton()
        b.setIcon(QIcon(os.path.join(self.parent.path_images, iconFileName)))
        b.setIconSize(iconSize)
        b.clicked.connect(lambda: self.move(actionId))
        return b
    
    def createQLabel(self, text, font=QApplication.font(), alignment=Qt.AlignCenter):
        label = QLabel()
        label.setText(text)
        label.setFont(font)
        label.setAlignment(alignment)
        return label
    
    def createQGraphicsLineItem(self, x1, y1, x2, y2):
        pen = QPen(Qt.black)
        pen.setWidth(2)
        line = QGraphicsLineItem(x1, y1, x2, y2)
        line.setPen(pen)
        line.setFlag(QGraphicsItem.ItemIsMovable, False)
        line.setFlag(QGraphicsItem.ItemIsSelectable, False)
        return line

    @asyncSlot()
    async def move(self, actionId):
        board = self.parent.board
        if board is None:
            return

        if self.moveObject:
            if actionId==1:
                self.moveObject.move(-10, 0)
            elif actionId==10:
                self.moveObject.move(10, 0)
            elif actionId==20:
                self.moveObject.move(0, 10)
            elif actionId==30:
                self.moveObject.move(0, -10)

        motorIndex = 0
        moveSign = 1
        if actionId==1:
            motorIndex = 0
        elif actionId==10:
            motorIndex = 0
            moveSign = -1
        elif actionId==20:
            motorIndex = 1
        elif actionId==30:
            motorIndex = 1
            moveSign = -1
        elif actionId==40:
            motorIndex = 2
        elif actionId==50:
            motorIndex = 2
            moveSign = -1

        motorName = self.parent.motorNames[motorIndex]
        step = moveSign * int(self.parent.preference.get(motorName, 'step'))
        motor = self.parent.motors[motorName]

        speed = int(self.parent.preference.get(motorName, "speed"))
        await self.board.stepper_set_speed(motor, speed)
        maxSpeed = int(self.parent.preference.get(motorName, "maxSpeed"))
        await self.board.stepper_set_max_speed(motor, maxSpeed)
        acceleration = int(self.parent.preference.get(motorName, "acceleration"))
        await self.board.stepper_set_acceleration(motor, acceleration)

        await self.moveImpl(motor, step)
        
    async def moveImpl(self, motor, step):    
        #self.parent.backgroundActions(4)
        await self.board.stepper_move(motor, step)
        await self.board.stepper_get_current_position(motor, self.current_position_callback)
        await self.board.stepper_get_target_position(motor, self.target_position_callback)
        await self.board.stepper_get_distance_to_go(motor, self.distance_to_go_callback)
        await self.board.stepper_is_running(motor, self.is_running_callback)
        await self.board.stepper_run(motor, completion_callback=self.the_callback)

    async def the_callback(self, data):
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[2]))
        print(f'Motor {data[1]} relative  motion completed at: {date}.')
    
    async def current_position_callback1(self, data):
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[2]))
        print(f'Motor {data[1]} relative  motion completed at: {date}.')
    
    async def current_position_callback(self, data):
        print(f'current_position_callback returns {data[2]}\n')


    async def target_position_callback(self, data):
        print(f'target_position_callback returns {data[2]}')


    async def distance_to_go_callback(self, data):
        print(f'distance_to_go_callback returns {data[2]}\n')


    async def is_running_callback(self, data):
        print(f'is_running_callback returns {data[1]}\n')
    
    
    