# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 09:54:20 2020

@author: Earthman
"""



import ctypes as ct
import tkinter as tk
from win32api import GetSystemMetrics

#   GUI OBJECT

class EUVGUI(object):

    def __init__(self):
        
        #----VARIALBES----------------------------------------------------------
        
        #   C Library Object
        self.OmsLib = Oms(self)
        #   Log
        self.guiLog = self.OmsLib.log
        #   String for commands to be sent
        self.commandSend = ""
        #   Padding
        self.pad = 3
        #   Screen Width & Height
        self.screenWidth = GetSystemMetrics(0)
        self.screenHeight = GetSystemMetrics(1)
        
       
        #----CREATE WIDGETS-----------------------------------------------------
        
        #   GUI Window
        self.root = tk.Tk()
        self.root.title("EUV Motor's Graphical User Interface")
        #   Maximizes window
        #self.root.state('zoomed')
        
        #   Padding
        self.root['padx'] = self.pad
        self.root['pady'] = self.pad        
        
        #   Main canvas
        self.mainCanvas = tk.Canvas(self.root, relief = "sunken")
        #   Scrollbars
        self.yScroll = tk.Scrollbar(self.mainCanvas, command = self.mainCanvas.yview)
        self.xScroll = tk.Scrollbar(self.mainCanvas, command = self.mainCanvas.xview, orient = "horizontal")
        #   Config scrollbars on canvas
        self.mainCanvas['yscrollcommand'] = self.yScroll.set
        self.mainCanvas['xscrollcommand'] = self.xScroll.set

        #   Purple Dot
        self.purpleDotParent = tk.Canvas(self.mainCanvas, height = 50, width = 50)
        self.purpleDot = self.purpleDotParent.create_oval(2, 2, 48, 48, fill = "MediumPurple")
        
        #   Main Frame
        self.mainFrame = tk.LabelFrame(self.mainCanvas, text = "Main Frame", relief = "ridge")
        self.mainFrame['padx'] = self.pad
        self.mainFrame['pady'] = self.pad
 
        #   Controller Model
        self.modelLabel = tk.Label(self.mainFrame, text = "Controller Model: " + str(self.OmsLib.model.value))

        #   Send Command Frame
        self.commandFrame = tk.LabelFrame(self.mainFrame, text = "Send command to controller:", relief = "ridge")
        #   Entry
        self.command = tk.Entry(self.commandFrame, width = 10)
        self.command.pack(side = "top")
        #   Button
        self.commandButton = tk.Button(self.commandFrame, text = "Send", command = lambda : [self.OmsLib.sendCommand(str(self.command.get())), self.updateLog()])
        self.commandButton.pack(side = "bottom")

        #   Reset Button. Updates the log regarding if reset was successful or not
        self.resetButton = tk.Button(self.mainFrame, text = "Reset Controller", command = lambda : [self.OmsLib.resetController(), self.updateLog()])

        #   Controller Log Frame
        self.logLabelFrame = tk.LabelFrame(self.mainCanvas, text = "Controller Log", relief = "ridge")
        self.logLabelFrame['padx'] = self.pad
        self.logLabelFrame['pady'] = self.pad
        #   Text
        self.logText = tk.Text(self.logLabelFrame, height = 46, width = 50)
        self.logText.insert(tk.END, self.guiLog)
        #   Scrollbar
        self.textScrollBar = tk.Scrollbar(self.logLabelFrame, command = self.logText.yview)
        self.logText['yscrollcommand'] = self.textScrollBar.set
        
        #   Motors Frame
        self.motorsFrame = tk.LabelFrame(self.mainCanvas, text = "Motors", relief = "ridge")
        self.motorsFrame['padx'] = self.pad
        self.motorsFrame['pady'] = self.pad
        
        
        #---PLACEMENTS--------------------------------------------------------
        #   Root
        self.mainCanvas.pack(fill = "both", expand = True)
        
        
        #   Main Canvas
        self.yScroll.pack(side = "right", fill = "y")
        self.xScroll.pack(side = "bottom", fill = "x")
        self.purpleDotParent.pack()
        self.mainFrame.pack()
        self.logLabelFrame.pack(side = "left")
        self.motorsFrame.pack(side = "right")
        
        
        #   Main Frame
        self.modelLabel.grid(row = 0, column = 0)
        self.commandFrame.grid(row = 0, column = 1)
        self.resetButton.grid(row = 0, column = 2)
        
        #   Log Frame
        self.logText.grid(row = 0, column = 0)
        self.textScrollBar.grid(row = 0, column = 1, sticky = "ns")
        
        
        #   For loop for creating the motors
        currRow = 0
        currCol = 0
        
        for motorNum in range(1,8):
            
            motorNumStr = str(motorNum)
            
            # Frame
            motorFrame = tk.LabelFrame(self.motorsFrame, text = "Motor #" + motorNumStr, relief = "ridge")
            motorFrame.grid(row = currRow, column = currCol)

            # Motor Position
            motorPos = tk.Label(motorFrame, text = ("Axis #" + motorNumStr + " motor position: " + str(self.OmsLib.getMotorAxisPosition(motorNumStr))))

            # Motor commands
            motorLabel = tk.Label(motorFrame, text = "Enter number of steps to move relative to its position:")
            # Entry
            motorEntry = tk.Entry(motorFrame, width = 10)
            # Send button
            motorButton = tk.Button(motorFrame, text = "Send", command = lambda n = motorNum, entry = motorEntry : [self.OmsLib.moveOmsAxisRelativeWait(n, int(entry.get())), self.updateLog()])

            # Base veloctiy controls
            baseVelocityLabel = tk.Label(motorFrame, text = "Set base velocity:")
            # Entry
            baseVelocityEntry = tk.Entry(motorFrame, width = 10)
            # Button
            baseVelocityButton = tk.Button(motorFrame, text = "Set", command = lambda n = motorNum, entry = baseVelocityEntry  : [self.OmsLib.setAxisBaseVelocity(n, int(entry.get())), self.updateLog()])

            # Velocity control options
            velocityLabel = tk.Label(motorFrame, text = "Set velocity:")
            # Entry
            velocityEntry = tk.Entry(motorFrame, width = 10)
            # Button
            velocityButton = tk.Button(motorFrame, text = "Set", command = lambda n = motorNum, entry = velocityEntry  : [self.OmsLib.setAxisVelocity(n, int(entry.get())), self.updateLog()])

            # Acceleration control options
            accelerationLabel = tk.Label(motorFrame, text = "Set acceleration:")
            # Entry
            accelerationEntry = tk.Entry(motorFrame, width = 10)
            # Button
            accelerationButton = tk.Button(motorFrame, text = "Set", command = lambda n = motorNum, entry = accelerationEntry  : [self.OmsLib.setAxisAcceleration(n, int(entry.get())), self.updateLog()])
            
            
            #---PLACEMENTS----------------------------------------------------
            #   Motor
            motorPos.grid(row = 0, column = 1)
            motorLabel.grid(row = 1, column = 0)
            motorEntry.grid(row = 2, column = 0)
            motorButton.grid(row = 3, column = 0)
            #   Base Velocity
            baseVelocityLabel.grid(row = 1, column = 1)
            baseVelocityEntry.grid(row = 2, column = 1)
            baseVelocityButton.grid(row = 3, column = 1)
            #   Velocity
            velocityLabel.grid(row = 1, column = 2)
            velocityEntry.grid(row = 2, column = 2)
            velocityButton.grid(row = 3, column = 2)
            #   Acceleration
            accelerationLabel.grid(row = 1, column = 3)
            accelerationEntry.grid(row = 2, column = 3)
            accelerationButton.grid(row = 3, column = 3)

            currRow += 1
        
        
        #   Update log at the very end
        self.updateLog()

#--------------------------------------------------------------------------------------------------

    #   GUI function to update the log on the screen
    def updateLog(self):
        
        self.logText.delete(1.0, tk.END)
        self.logText.insert(tk.END, self.OmsLib.getLog())
   

################################################################################################################################
################################################################################################################################
################################################################################################################################


#   OMS CONTROLLER OBJECT, INHERITS GUI OBJECT
class Oms(object):

    def __init__(self, gui):

        #   GLOBAL VARIABLES

        #   GUI OBJECT
        self.gui = gui

        #   OMS LIBRARY
        self.lib = ct.WinDLL("./Important_Files/MAXkSoftware/MAXkWebsiteWindows10/lib/Win10/x64/OmsMAXkMC.dll")
        print("lib: ", self.lib)
        
        #   CREATE MUTATABLE CHARACTER BUFFER, RETURNS C_CHAR. h IS A LIST, pt IS CTYPES.C_CHAR_P
        h = [ct.create_string_buffer(b"OmsMAXk1")]
        
        #######################################################################
        #   pt DECLARES ITSELF AS C_CHAR_P VARIABLE 
        #    * ALLOWS FOR VARIABLE NUMBER OF ARGUMENTS TO BE PASSED
        #   map() LOOPS THROUGH FUNCTION ct.addressof WITH h BEING ONLY INTERABLE.
        #   ct.addressof() RETURNS ADDRESS OF h AS AN INT
        #######################################################################
        pt = (ct.c_char_p)(*map(ct.addressof, h))

        self.handle = self.lib.GetOmsHandle(pt)
        print("handle: ", self.handle)
        
        #   CONTROLLER LOG
        self.log = ""

        #   OMS CONTROLLER MODEL
        self.model = self.getModel()

        #   TRUE OR FALSE VALUE DETERMINING IF DRIVERS WERE LOADED
        self.libConnection = self.checkLibrary()

       

#--------------------------------------------------------------------------------------------------

       
    def getModel(self):

        self.addLog("Attempting to retrieve model...")

        #   MODEL VARIABLE DECLARED AS A C STRING BUFFER
        model = ct.create_string_buffer(80)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        
        c_retVal = self.lib.GetOmsControllerDescription( self.handle, model)
        
        self.handleReturnValue(c_retVal)
        

        return model

 
#--------------------------------------------------------------------------------------------------
        

    def checkLibrary(self):
        
        #   Checking to see if drivers are loaded
        if(self.handle == 0):
            self.addLog("-Driver for device was not loaded.")
            return False

        else:
            self.addLog("-Drivers loaded successfully")
            return True
 

#--------------------------------------------------------------------------------------------------


    def sendCommand(self, arg):

        self.addLog("Attempting to send command: " + str(arg))
        
        returnStatus = 0
        c_returnStatus = ct.c_long(returnStatus)
        
        c_arg = ct.create_string_buffer(bytes(arg,'utf-8'))
        
        #######################################################################
        #   Runs a check if to see if command sends a string back using
        #   SendAndGetString function. If response_time_out is returned, it will
        #   send command using the SendString function that does not return a string
        #######################################################################
        c_returnStatus = self.lib.SendAndGetString(self.handle, c_arg)
        
        #   A return value of 2 signals a response time out
        if(c_returnStatus == 2):
            c_returnStatus = self.lib.SendString(self.handle, c_arg)
            self.handleReturnValue(c_returnStatus)

        #   If no time out, function prints return status followed by the returned string
        else:
            self.handleReturnValue(c_returnStatus)
            self.addLog(c_arg)

#--------------------------------------------------------------------------------------------------


    def getLog(self):

        return self.log


#--------------------------------------------------------------------------------------------------


    def addLog(self, arg):

        self.log = self.getLog() + str(arg) + "\n"
        

#--------------------------------------------------------------------------------------------------


    def resetController(self):
        
        self.addLog("Attempting to reset controller...")

        resetStatus = self.lib.ResetOmsController(self.handle)

        #   Logs reset status
        self.handleReturnValue(resetStatus)

           
#--------------------------------------------------------------------------------------------------


    def closeHandle(self):
        
        self.lib.CloseOmsHandle(self.handle)
        
        
#--------------------------------------------------------------------------------------------------
        
        
    def setAxisBaseVelocity(self, axis, velocity):
        
        self.addLog("Attempting to set axis #" + str(axis) + " base velocity...")
        
        self.axis = axis
        self.velocity = velocity
        
        #   Determine which axis is being called
        axisAsInt = self.determineAxisAsInt(self.axis)
        
        c_axis = ct.c_long(axisAsInt)
        c_velocity = ct.c_long(self.velocity)
        

        #   Check to see if base velocity input is less than max velocity
        velocityCheck = 0
        c_velocityCheck = ct.c_long(velocityCheck)
        
        self.lib.GetOmsAxisVelocity(self.handle, c_axis, c_velocityCheck)
        
        velocityCheck = c_velocityCheck.value
        
        if(self.velocity < velocityCheck):
            self.addLog("Base velocity must be less than max velocity")
            self.addLog("Max velocity currently set to: " + velocityCheck)
            
        else:
            retVal = 0
            c_retVal = ct.c_long(retVal)
            
            c_retVal = self.lib.SetOmsAxisBaseVelocity(self.handle, c_axis, c_velocity)
            
            
            #   ERROR HANDLING
            self.handleReturnValue(c_retVal)
                
            
#--------------------------------------------------------------------------------------------------
    
    def setAxisVelocity(self, axis, velocity):
        
        self.addLog("Attempting to set axis #" + str(axis) + " velocity...")
        
        self.axis = axis
        self.velocity = velocity
        
        #   Determine which axis is being called
        axisAsInt = self.determineAxisAsInt(self.axis)
        
        c_axis = ct.c_long(axisAsInt)
        c_velocity = ct.c_long(self.velocity)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        c_retVal = self.lib.SetOmsAxisVelocity(self.handle, c_axis, c_velocity)
        
        
        #   ERROR HANDLING
        self.handleReturnValue(c_retVal)
        
        
#--------------------------------------------------------------------------------------------------
            
    def setAxisAcceleration(self, axis, acceleration):
              
        self.addLog("Attempting to set axis #" + str(axis) + " acceleration...")
        
        if (acceleration < 1 or acceleration > 8000000):
            self.addLog("Value must be between 1 - 8,000,000")
            
        else:
        
            self.axis = axis
            self.acceleration = acceleration
            
            #   Determine which axis is being called
            axisAsInt = self.determineAxisAsInt(self.axis)
        
            c_axis = ct.c_long(axisAsInt)
            c_acceleration = ct.c_long(self.acceleration)
            
            retVal = 0
            c_retVal = ct.c_long(retVal)
            c_retVal = self.lib.SetOmsAxisAcceleration(self.handle, c_axis, c_acceleration)
            
            
            #   ERROR HANDLING
            self.handleReturnValue(c_retVal)
            
            
#--------------------------------------------------------------------------------------------------
            
    def getMotorAxisPosition(self, axis):
        
        self.addLog("Attempting to retrieve axis #" + str(axis) + " position...")
        
        #   axis variable type is a string
        self.axis = axis
        
        #   Determine axis is being called
        axisAsInt = self.determineAxisAsInt(self.axis)
        
        c_axis = ct.c_long(axisAsInt)
        
        position = 0
        c_position = ct.c_long(position)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        
        #################################################################################################
        #   ct.byref creates a psuedo-pointer to the object passed in as an argument,
        #   in this case it creates a "pointer" to a long, which GetOmsAxisMotorPosition uses to fill-in
        #   the underlying long with the motor position 
        #################################################################################################
        c_retVal = self.lib.GetOmsAxisMotorPosition(self.handle, c_axis, ct.byref(c_position))
        
        #   ERROR HANDLING
        self.handleReturnValue(c_retVal)
        
        position = ct.c_long(position).value
        
        return position
            
#--------------------------------------------------------------------------------------------------
            
    def moveOmsAxisRelativeWait(self, axis, position):
        
        self.addLog("Attempting to move axis #" + str(axis) + " " + str(position) + " steps...")
        
        self.axis = self.determineAxisAsInt(axis)
        self.position = position
        
        #   Setting time limit so that it will wait 5 seconds before signaling time out, is measured in milliseconds
        timeLim = 5000
        c_timeLim = ct.c_long(timeLim)
        
        c_axis = ct.c_long(self.axis)
        
        #   position variable is sent over as a string but needs to be an int to convert to long
        position = int(self.position)
        c_position = ct.c_long(position)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        
        c_retVal = self.lib.MoveOmsAxisRelWait(self.handle, c_axis, c_position, c_timeLim)
        
        
        #   ERROR HANDLING
        self.handleReturnValue(c_retVal)

            
#--------------------------------------------------------------------------------------------------
            
    def handleReturnValue(self, returnValue):
        
        self.returnValue = returnValue
        
        if (self.returnValue == 0):
            self.addLog("-Success")
            
        elif(self.returnValue == 1):
            self.addLog("-Command time out")
            
        elif(self.returnValue == 2):
            self.addLog("-Response time out")
        
        elif(self.returnValue == 3):
            self.addLog("-Invalid axis selection")
        
        elif(self.returnValue == 4):
            self.addLog("-Move time out")
            
        elif(self.returnValue == 5):
            self.addLog("-Invalid parameter")
            
        elif(self.returnValue == 6):
            self.addLog("-Invalid bit number")
            
        else:
            self.addLog("-Value does not fall under OMS source code return values")
            
            
#--------------------------------------------------------------------------------------------------
            
    def determineAxisAsInt(self, axis):
        
        self.axis = axis
        
        if(self.axis == "1" or self.axis == 1):
            axisAsInt = 1
            
        elif(self.axis == "2" or self.axis == 2):
            axisAsInt = 2
            
        elif(self.axis == "3" or self.axis == 3):
            axisAsInt = 4
            
        elif(self.axis == "4" or self.axis == 4):
            axisAsInt = 8
            
        elif(self.axis == "5" or self.axis == 5):
            axisAsInt = 16
            
        elif(self.axis == "6" or self.axis == 6):
            axisAsInt = 32

        elif(self.axis == "7" or self.axis == 7):
            axisAsInt = 64
            
        else:
            self.addLog("Axis not recognized, setting to 0")
            axisAsInt = 0
            
        return axisAsInt
        
        
################################################################################################################################
################################################################################################################################


def main():

 
    #   GUI object
    EUV = EUVGUI()

    #   Run GUI main loop
    EUV.root.mainloop()
    
    #   Close handle
    EUV.OmsLib.closeHandle()
   
    print("End of program")


#--------------------------------------------------------------------------------------------------


#DRIVER CODE

if __name__ == '__main__' :

    main()
    
#--------------------------------------------------------------------------------------------------