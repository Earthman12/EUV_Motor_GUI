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
        self.mainCanvas = tk.Canvas(self.root, relief = "ridge")

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
        self.logText = tk.Text(self.logLabelFrame, height = 15, width = 50)
        self.logText.insert(tk.END, self.guiLog)
        #   Scrollbar
        self.textScrollBar = tk.Scrollbar(self.logLabelFrame, command = self.logText.yview)
        self.logText['yscrollcommand'] = self.textScrollBar.set
        
        #   Motors Frame
        self.motorsFrame = tk.LabelFrame(self.mainCanvas, text = "Motors", relief = "ridge")
        self.motorsFrame['padx'] = self.pad
        self.motorsFrame['pady'] = self.pad
        
        #   Frame to select which motor
        self.motorSelectFrame = tk.LabelFrame(self.motorsFrame, text = "Select Motor", relief = "ridge")
        #   Variable for motor selection
        self.motor = tk.IntVar()
        
        #   Radio buttons to select the motor
        self.rButton1 = tk.Radiobutton(self.motorSelectFrame, text = ("Motor 1 - Position: " + str(self.OmsLib.getMotorAxisPosition(1))), variable = self.motor, value = 1)
        self.rButton2 = tk.Radiobutton(self.motorSelectFrame, text = ("Motor 2 - Position: " + str(self.OmsLib.getMotorAxisPosition(2))), variable = self.motor, value = 2)
        self.rButton3 = tk.Radiobutton(self.motorSelectFrame, text = ("Motor 3 - Position: " + str(self.OmsLib.getMotorAxisPosition(3))), variable = self.motor, value = 3)
        self.rButton4 = tk.Radiobutton(self.motorSelectFrame, text = ("Motor 4 - Position: " + str(self.OmsLib.getMotorAxisPosition(4))), variable = self.motor, value = 4)
        self.rButton5 = tk.Radiobutton(self.motorSelectFrame, text = ("Motor 5 - Position: " + str(self.OmsLib.getMotorAxisPosition(5))), variable = self.motor, value = 5)
        self.rButton6 = tk.Radiobutton(self.motorSelectFrame, text = ("Motor 6 - Position: " + str(self.OmsLib.getMotorAxisPosition(6))), variable = self.motor, value = 6)
        self.rButton7 = tk.Radiobutton(self.motorSelectFrame, text = ("Motor 7 - Position: " + str(self.OmsLib.getMotorAxisPosition(7))), variable = self.motor, value = 7)
        
        #   Motor commands frame
        self.motorCommandFrame = tk.LabelFrame(self.motorsFrame, text = "Motor Commands", relief = "ridge")
        
        #   Step commands
        self.stepsLabel = tk.Label(self.motorCommandFrame, text = "Enter number of steps to move relative to its position:")
        #   Entry
        self.stepsEntry = tk.Entry(self.motorCommandFrame, width = 10)
        #   Send button
        self.stepsButton = tk.Button(self.motorCommandFrame, text = "Send", command = lambda : [self.OmsLib.moveOmsAxisRelativeWait(self.motor.get(), int(self.stepsEntry.get())), self.updateLog()])

        #   Base veloctiy controls
        self.baseVelocityLabel = tk.Label(self.motorCommandFrame, text = "Set base velocity:")
        #   Entry
        self.baseVelocityEntry = tk.Entry(self.motorCommandFrame, width = 10)
        #   Set Button
        self.baseVelocityButton = tk.Button(self.motorCommandFrame, text = "Set", command = lambda : [self.OmsLib.setAxisBaseVelocity(self.motor.get(), int(self.baseVelocityEntry.get())), self.updateLog()])

        #   Velocity control options
        self.velocityLabel = tk.Label(self.motorCommandFrame, text = "Set velocity:")
        #   Entry
        self.velocityEntry = tk.Entry(self.motorCommandFrame, width = 10)
        #   Set Button
        self.velocityButton = tk.Button(self.motorCommandFrame, text = "Set", command = lambda : [self.OmsLib.setAxisVelocity(self.motor.get(), int(self.velocityEntry.get())), self.updateLog()])
        #   Get Button
        self.velocityButton2 = tk.Button(self.motorCommandFrame, text = "Get", command = lambda : [self.OmsLib.getAxisVelocity(self.motor.get()), self.updateLog()])

        #   Acceleration control options
        self.accelerationLabel = tk.Label(self.motorCommandFrame, text = "Set acceleration:")
        #   Entry
        self.accelerationEntry = tk.Entry(self.motorCommandFrame, width = 10)
        #   Set Button
        self.accelerationButton = tk.Button(self.motorCommandFrame, text = "Set", command = lambda : [self.OmsLib.setAxisAcceleration(self.motor.get(), int(self.accelerationEntry.get())), self.updateLog()])
        #   Get Button
        self.accelerationButton2 = tk.Button(self.motorCommandFrame, text = "Get", command = lambda : [self.OmsLib.getAxisAcceleration(self.motor.get()), self.updateLog()])
        
        #---PLACEMENTS--------------------------------------------------------
        #   Root
        self.mainCanvas.pack(fill = "both", expand = True)
        
        #   Main Canvas
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

        #   Motors Frame
        self.motorSelectFrame.pack()
        self.motorCommandFrame.pack()
        
        #   Motor Select Frame
        self.rButton1.grid(row = 0, column = 0)
        self.rButton2.grid(row = 1, column = 0)
        self.rButton3.grid(row = 2, column = 0)
        self.rButton4.grid(row = 3, column = 0)
        self.rButton5.grid(row = 0, column = 1)
        self.rButton6.grid(row = 1, column = 1)
        self.rButton7.grid(row = 2, column = 1)
        
        #   Motor Command Frame
        #   Steps
        self.stepsLabel.grid(row = 1, column = 0)
        self.stepsEntry.grid(row = 2, column = 0)
        self.stepsButton.grid(row = 3, column = 0)
        #   Base Velocity
        self.baseVelocityLabel.grid(row = 1, column = 1)
        self.baseVelocityEntry.grid(row = 2, column = 1)
        self.baseVelocityButton.grid(row = 3, column = 1)
        #   Velocity
        self.velocityLabel.grid(row = 1, column = 2)
        self.velocityEntry.grid(row = 2, column = 2)
        self.velocityButton.grid(row = 3, column = 2)
        self.velocityButton2.grid(row = 4, column = 2)
        #   Acceleration
        self.accelerationLabel.grid(row = 1, column = 3)
        self.accelerationEntry.grid(row = 2, column = 3)
        self.accelerationButton.grid(row = 3, column = 3)
        self.accelerationButton2.grid(row = 4, column = 3)
        #---------------------------------------------------------------------
        
        #   Update log at the very end
        self.updateLog()

#--------------------------------------------------------------------------------------------------

    #   GUI function to update the log on the screen
    def updateLog(self):
        
        self.logText.delete(1.0, tk.END)
        self.logText.insert(tk.END, self.OmsLib.getLog())
        self.logText.yview("end")
   

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
        
        resetStatus = 0
        c_resetStatus = ct.c_long(resetStatus)

        c_resetStatus = self.lib.ResetOmsController(self.handle)

        #   Logs reset status
        self.handleReturnValue(c_resetStatus)

           
#--------------------------------------------------------------------------------------------------


    def closeHandle(self):
        
        self.lib.CloseOmsHandle(self.handle)
        
        
#--------------------------------------------------------------------------------------------------
        
        
    def setAxisBaseVelocity(self, axis, velocity):
        
        self.addLog("Attempting to set axis #" + str(axis) + " base velocity...")
        
        #   Determine which axis is being called
        axisAsInt = self.determineAxisAsInt(axis)
        
        c_axis = ct.c_long(axisAsInt)
        c_velocity = ct.c_long(velocity)
        

        #   Check to see if base velocity input is less than max velocity
        velocityCheck = 0
        c_velocityCheck = ct.c_long(velocityCheck)
        
        self.lib.GetOmsAxisVelocity(self.handle, c_axis, c_velocityCheck)
        
        velocityCheck = c_velocityCheck.value
        
        if(velocity < velocityCheck):
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
        
        #   Determine which axis is being called
        axisAsInt = self.determineAxisAsInt(axis)
        
        c_axis = ct.c_long(axisAsInt)
        c_velocity = ct.c_long(velocity)
        
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
            
            #   Determine which axis is being called
            axisAsInt = self.determineAxisAsInt(axis)
        
            c_axis = ct.c_long(axisAsInt)
            c_acceleration = ct.c_long(acceleration)
            
            retVal = 0
            c_retVal = ct.c_long(retVal)
            c_retVal = self.lib.SetOmsAxisAcceleration(self.handle, c_axis, c_acceleration)
            
            
            #   ERROR HANDLING
            self.handleReturnValue(c_retVal)
            
            
#--------------------------------------------------------------------------------------------------
            
    def getMotorAxisPosition(self, axis):
        
        self.addLog("Attempting to retrieve axis #" + str(axis) + " position...")
        
        #   Determine axis is being called
        axisAsInt = self.determineAxisAsInt(axis)
        
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
        
        axisAsInt = self.determineAxisAsInt(axis)
        
        #   Setting time limit so that it will wait 5 seconds before signaling time out, is measured in milliseconds
        timeLim = 5000
        c_timeLim = ct.c_long(timeLim)
        
        c_axis = ct.c_long(axisAsInt)
        
        #   position variable is sent over as a string but needs to be an int to convert to long
        position = int(position)
        c_position = ct.c_long(position)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        
        c_retVal = self.lib.MoveOmsAxisRelWait(self.handle, c_axis, c_position, c_timeLim)
        
        
        #   ERROR HANDLING
        self.handleReturnValue(c_retVal)

            
#--------------------------------------------------------------------------------------------------
            
    def handleReturnValue(self, returnValue):
        
        if (returnValue == 0):
            self.addLog("-Success")
            
        elif(returnValue == 1):
            self.addLog("-Command time out")
            
        elif(returnValue == 2):
            self.addLog("-Response time out")
        
        elif(returnValue == 3):
            self.addLog("-Invalid axis selection")
        
        elif(returnValue == 4):
            self.addLog("-Move time out")
            
        elif(returnValue == 5):
            self.addLog("-Invalid parameter")
            
        elif(returnValue == 6):
            self.addLog("-Invalid bit number")
            
        else:
            self.addLog("-Value does not fall under OMS source code return values")
            
            
#--------------------------------------------------------------------------------------------------
            
    def determineAxisAsInt(self, axis):
        
        if(axis == "1" or axis == 1):
            axisAsInt = 1
            
        elif(axis == "2" or axis == 2):
            axisAsInt = 2
            
        elif(axis == "3" or axis == 3):
            axisAsInt = 4
            
        elif(axis == "4" or axis == 4):
            axisAsInt = 8
            
        elif(axis == "5" or axis == 5):
            axisAsInt = 16
            
        elif(axis == "6" or axis == 6):
            axisAsInt = 32

        elif(axis == "7" or axis == 7):
            axisAsInt = 64
            
        else:
            self.addLog("Axis not recognized, setting to 0")
            axisAsInt = 0
            
        return axisAsInt
        
        
#--------------------------------------------------------------------------------------------------
        
    def getAxisVelocity(self, axis):
        
        self.addLog("Attempting to retrieve velocity for motor #" + str(axis))
        
        axisAsInt = self.determineAxisAsInt(axis)
        
        c_axis = ct.c_long(axisAsInt)
        
        velocity = 0
        c_velocity = ct.c_long(velocity)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        
        c_retVal = self.lib.GetOmsAxisVelocity(self.handle, c_axis, c_velocity)
        
        self.handleReturnValue(c_retVal)
        
        velocity = ct.c_long(velocity).value
        
        return velocity
        
        
#--------------------------------------------------------------------------------------------------
        
    def getAxisAcceleration(self, axis):
        
        self.addLog("Attempting to retrieve acceleration for motor #" + str(axis))

        axisAsInt = self.determineAxisAsInt(axis)
        c_axis = ct.c_long(axisAsInt)
        
        acceleration = 0
        c_acceleration = ct.c_long(acceleration)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        
        c_retVal = self.lib.GetOmsAxisAcceleration(self.handle, c_axis, c_acceleration)
        
        self.handleReturnValue(c_retVal)
        
        acceleration = ct.c_long(acceleration).value
        
        return acceleration
    

        
        
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