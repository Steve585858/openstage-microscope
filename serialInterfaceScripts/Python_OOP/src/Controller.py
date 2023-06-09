
import re
import serial

# Main window class
class Controller():
    def __init__(self):
        super().__init__() 
        #change serial port number in following line to that you are using 
        self.ser=serial.Serial(3, baudrate=115200, timeout=2)
    
    def write(self, strToSend):
        self.ser.write(strToSend)
    
    def close(self):
        self.ser.close()
    
    def flushInput(self):
        self.ser.flushInput()
        
    def readBuffer(self):
        c=self.ser.read()
        thisStr=''
        while c is not '$':
            thisStr += c
            c=self.ser.read()
        return thisStr
    
    def readAndPrintBuffer(self):
        print('\n' + self.readBuffer() + '\n')
    
    def beep(self):
        self.write("b")
    
    def getInfo(self):
        self.flushInput() 
        self.write("i")
        self.readAndPrintBuffer()

    #Obtain stage location on each axis and display on screen
    def getPosition(self):
        self.flushInput() 
        self.write("p")
        self.readAndPrintBuffer()
    
    # Purpose
    # Moves OpenStage to a defined absolute or relative position.
    # Inputs 
    # coords - Desired position of each axis in microns. All axes must be
    #          set. By convention axes are ordered: x,y,z.  
    # motionType [optional]- a character 'a' [default] or 'r' for absolute or relative. 
    #
    #
    # Examples
    # OS_goto([0,200.5,0])   %moves to position X: 0, Y: 200.5, Z: 0
    # OS_goto([0,0,-10],'r') %relative move of -10 microns in Z
    #
    #
    # Notes
    # - Signed values are possible and influence direction of motion. The 
    # way the system is wired determines the motion direction.
    # - coords are transmitted over the serial line as
    # integers (not binary). The three least significant digits are after the decimal
    # point. This function takes care of this automatically.  So if we want the stage to 
    # move 1.5 microns, this routine submits 1500 to the controller. However, the user
    # supplies the value "1.5"
    # - The function induces a blocking pause until motion is complete. 

    def goto(self, x, y, z, motionType='a'):
        #Build string to send to controller
        strToSend='g' + motionType
        for arg in [x,y,z]:
            thisNumber=int(round(float(arg)*1000))
            strToSend += str(thisNumber) + ','

        strToSend=strToSend[:-1] + '$'

        self.flushInput()
        self.write(strToSend)
        #Now block and wait for terminator
        self.readAndPrintBuffer()
        
    # Purpose
    # Set or read the speed parameter of each axis. If no
    # inputs are provided, prints values to screen. If three inputs 
    # are provided, the function uses these to set the speed 
    # parameters on the stage. Parameters relate to Go To serial 
    # motions and right-button motions only. 
    #
    #
    # Inputs
    # Three numbers defining the speed in microns per second for 
    # Axes ordered X,Y,Z and all must be provided.
    #
    # Examples
    # OS_moveSpeed     #prints axes speeds to screen
    # OS_moveAccel 500 500 1000 #set speeds in X, Y, and Z
    #
    def getSpeed(self):
        self.flushInput() 
        self.write('vr')
        buf=self.readBuffer()
        numAxes=len([m.start() for m in re.finditer(',', buf)]) + 1
        print('\n' + buf + '\n')

    def setSpeed(self, x, y, z):
        #Build string to send
        strToSend='vs'
        for arg in [x,y,z]:
            arg = int(arg)
            strToSend += str(arg) + ','
        strToSend=strToSend[:-1] + '$'

        #Send string
        self.flushInput() 
        self.write(strToSend)
        self.readAndPrintBuffer()

    # Purpose
    # Set or read the acceleration parameter of each axis. If no
    # inputs are provided, prints values to screen. If three inputs 
    # are provided, the function uses these to set the acceleration 
    # parameters on the stage. Parameters relate to Go To serial 
    # motions and right-button motions only. 
    #
    #
    # Inputs
    # Three numbers defining the accelerations each axis in steps per s per s. 
    # Axes ordered X,Y,Z and all must be provided.
    #
    # Examples
    # OS_moveAccel     #prints axes accelerations to screen
    # OS_moveAccel 500 500 1000 #set accelerations in X, Y, and Z, unit is steps per second per second
    #
    def getAccel(self):
        self.flushInput() 
        self.write('ar')
        buf=self.readBuffer()
        numAxes=len([m.start() for m in re.finditer(',', buf)]) + 1
        print('\n' + buf + '\n')

    def setAccel(self, x, y, z):
        #Build string to send
        strToSend='as'
        for arg in [x,y,z]:
            arg = int(arg)
            strToSend += str(arg) + ','
        strToSend=strToSend[:-1] + '$'

        #Send string
        self.flushInput() 
        self.write(strToSend)
        self.readAndPrintBuffer()

    # Set Speed Mode on OpenStage 
    #
    # e.g. OS_setMode 3
    #
    # Purpose
    # Sets the Speed Mode for analog stick and D-pad motions on the OpenStage. 
    # This does not affect serial commands for Go To motions or return 
    # motions to locations stored on the right hand buttons.
    #
    #
    def getMode(self):
        self.flushInput()
        self.write('m')
        self.readAndPrintBuffer()

    def setMode(self, m):
        stepSize=int(stepSize)
        if int(m)>4 or int(m)<1:
            print('\n' + 'mode out of range' + '\n')
        else:
            self.flushInput()
            self.write("m" + m)
            self.readAndPrintBuffer()

    # Purpose 
    # Set or read (if no stepSize arg provided) the step sizes (in fractions 
    # of a full step) for all axes. All axes share the same step size.
    #
    # Inputs
    # stepSize - [optional] Sets a particular step size for right-button and
    #            serial port Go To motions. If stepSize is empty, the command
    #            returns the current step size of the controller. This is returned
    #            as a fraction of a full step. To define step size, the user 
    #            supplies an integer between 1 and 5. These correspond to the f
    #            following fractional step sizes:
    #            1 - full steps
    #            2 - 1/2
    #            3 - 1/4
    #            4 - 1/8
    #            5 - 1/16
    #
    #
    # Examples
    # OS_stepSize     #print current step size to screen
    # OS_stepSize 3   #set step size to 1/4 steps
    #
    def getStepSize(self):
        self.flushInput() #flush the buffer, to be safe
        self.write('sr')
        self.readAndPrintBuffer()

    def setStepSize(self, stepSize):
        stepSize=int(stepSize)
        if stepSize<1 or stepSize>5:
            print('\n' + 'stepSize out of range' + '\n')
        else:
            self.flushInput()
            self.write('ss' + str(stepSize))
            self.readAndPrintBuffer()

    # Zeros the stage position of the OpenStage
    #
    # Purpose
    # Zeros the position counters on the OpenStage LCD display. This also affects
    # the stage position value read back on the serial port. Any locations bound
    # To the right-hand buttons (triangle, square, etc) are retained, meaning that
    # the stage will seek back to the original stored physical location.
    #
    def zero(self):
        self.flushInput() #flush the buffer, to be safe
        self.write("z")
        self.readAndPrintBuffer()


