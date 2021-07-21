# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 09:54:20 2020

@author: Earthman
"""


import ctypes as ct
import tkinter as tk
import time
import math

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
        #   Grating position
        self.gratingPosition = self.OmsLib.gratingAngstromPosition
       
        #----CREATE WIDGETS-----------------------------------------------------
        
        #   GUI Window
        self.root = tk.Tk()
        self.root.title("EUV Motor's Graphical User Interface")
        
        #   Padding
        self.root['padx'] = self.pad
        self.root['pady'] = self.pad        
        
        #   Main canvas
        self.mainCanvas = tk.Canvas(self.root, relief = "ridge")
        
        #---Main Frame----------------------------------------------------------
        self.mainFrame = tk.LabelFrame(self.mainCanvas, text = "Main Frame", relief = "ridge")
        self.mainFrame['padx'] = self.pad
        self.mainFrame['pady'] = self.pad
        #   Controller model
        self.modelLabel = tk.Label(self.mainFrame, text = "Controller Model: " + str(self.OmsLib.model))
        #   Reset button
        self.resetButton = tk.Button(self.mainFrame, text = "Reset Controller", command = lambda : [self.OmsLib.resetController(), self.updateLog()])
        #---MCP Gate Valve Frame------------------------------------------------
        self.gateValveFrame = tk.LabelFrame(self.mainFrame, text = "MCP Gate Valve", relief = "ridge")
        self.gateOpenButton = tk.Button(self.gateValveFrame, text = "Open", command = lambda : [self.OmsLib.openMCPGate(), self.updateLog()])
        self.gateCloseButton = tk.Button(self.gateValveFrame, text = "Close", command = lambda : [self.OmsLib.closeMCPGate(), self.updateLog()])

        #---Controller Log Frame------------------------------------------------
        self.logLabelFrame = tk.LabelFrame(self.mainCanvas, text = "Controller Log", relief = "ridge")
        self.logLabelFrame['padx'] = self.pad
        self.logLabelFrame['pady'] = self.pad
        #   Text
        self.logText = tk.Text(self.logLabelFrame, height = 18, width = 50)
        self.logText.insert(tk.END, self.guiLog)
        #   Scrollbar
        self.textScrollBar = tk.Scrollbar(self.logLabelFrame, command = self.logText.yview)
        self.logText['yscrollcommand'] = self.textScrollBar.set
        
        #---Motors Frame--------------------------------------------------------
        self.motorsFrame = tk.LabelFrame(self.mainCanvas, text = "Motors", relief = "ridge")
        self.motorsFrame['padx'] = self.pad
        self.motorsFrame['pady'] = self.pad
        
        #---Motor Select Frame--------------------------------------------------
        self.motorSelectFrame = tk.LabelFrame(self.motorsFrame, text = "Select Motor", relief = "ridge")
        #   Variable for motor selection
        self.motor = tk.IntVar()
        
        #   Radio buttons to select the motor
        self.rButton1 = tk.Radiobutton(self.motorSelectFrame, text = ("Motor 1 - Position: " + str(self.OmsLib.getMotorAxisPosition(1))), variable = self.motor, value = 1)
        self.rButton2 = tk.Radiobutton(self.motorSelectFrame, text = ("Motor 2 - Position: " + str(self.OmsLib.getMotorAxisPosition(2))), variable = self.motor, value = 2)
        self.rButton3 = tk.Radiobutton(self.motorSelectFrame, text = ("Motor 3 - Position: " + str(self.OmsLib.getMotorAxisPosition(3))), variable = self.motor, value = 3)
        self.rButton4 = tk.Radiobutton(self.motorSelectFrame, text = ("Motor 4 - Position: " + str(self.OmsLib.getMotorAxisPosition(4))), variable = self.motor, value = 4)
        self.rButton6 = tk.Radiobutton(self.motorSelectFrame, text = ("Motor 6 - Position: " + str(self.OmsLib.getMotorAxisPosition(6))), variable = self.motor, value = 6)
        self.rButton7 = tk.Radiobutton(self.motorSelectFrame, text = ("Motor 7 - Position: " + str(self.OmsLib.getMotorAxisPosition(7))), variable = self.motor, value = 7)
        
        #---Grating Motor Frame-------------------------------------------------
        self.gratingFrame = tk.LabelFrame(self.motorsFrame, text = "Grating Motor", relief = "ridge")
        #   Home button
        self.homeButton = tk.Button(self.gratingFrame, text = "Home", command = lambda : [self.OmsLib.homeGrating(), self.gratingButtonToggle(), self.updateGratingPosition(0), self.updateLog()])
        #   Grating position
        self.gratingPosition = tk.Label(self.gratingFrame, text = ("Angstroms from  zero order: " + str(self.gratingPosition)))
        #   Move grating text label
        self.positionTextLabel = tk.Label(self.gratingFrame, text = "Set angstroms on the grating:")
        #   Grating entry
        self.gratingEntry = tk.Entry(self.gratingFrame, width = 10)
        #   Grating send button
        self.gratingButton = tk.Button(self.gratingFrame, text = "Set", command = lambda : [self.OmsLib.moveGrating(int(self.gratingEntry.get())), self.updateGratingPosition(self.gratingEntry.get()), self.updateLog()])
        #   Disabled on startup until grating is homed
        self.gratingButton["state"] = "disable"
        
        #---Motor commands frame------------------------------------------------
        self.motorCommandFrame = tk.LabelFrame(self.motorsFrame, text = "Motor Commands", relief = "ridge")
        
        #   Step commands
        self.stepsLabel = tk.Label(self.motorCommandFrame, text = "Enter number of steps to move relative to its position:")
        #   Entry
        self.stepsEntry = tk.Entry(self.motorCommandFrame, width = 10)
        #   Send button
        self.stepsButton = tk.Button(self.motorCommandFrame, text = "Set", command = lambda : [self.OmsLib.moveOmsAxisRelativeWait(self.motor.get(), int(self.stepsEntry.get())), self.updateMotorsPositions(self.motor.get()), self.updateLog()])

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
        self.mainFrame.pack()
        self.logLabelFrame.pack(side = "left")
        self.motorsFrame.pack(side = "right")
        
        #   Main Frame
        self.modelLabel.grid(row = 0, column = 0)
        self.resetButton.grid(row = 0, column = 2)
        self.gateValveFrame.grid(row = 0, column = 3)
        
        #   MCP Frame
        self.gateOpenButton.pack()
        self.gateCloseButton.pack()
        
        #   Log Frame
        self.logText.grid(row = 0, column = 0)
        self.textScrollBar.grid(row = 0, column = 1, sticky = "ns")

        #   Motors Frame
        self.gratingFrame.pack()
        self.motorSelectFrame.pack()
        self.motorCommandFrame.pack()

        #   Grating Frame
        self.homeButton.grid(row = 1, column = 0)
        self.gratingPosition.grid(row = 2, column = 0)
        self.positionTextLabel.grid(row = 0, column = 1)
        self.gratingEntry.grid(row = 1, column = 1)
        self.gratingButton.grid(row = 2, column = 1)
        
        #   Motor Select Frame
        self.rButton1.grid(row = 0, column = 0)
        self.rButton2.grid(row = 1, column = 0)
        self.rButton3.grid(row = 2, column = 0)
        self.rButton4.grid(row = 0, column = 1)
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
#----------------------------------GUI FUNCTIONS---------------------------------------------------
#--------------------------------------------------------------------------------------------------

    #   GUI function to update the log on the screen
    def updateLog(self):
        
        self.logText.delete(1.0, tk.END)
        self.logText.insert(tk.END, self.OmsLib.getLog())
        self.logText.yview("end")
        
#--------------------------------------------------------------------------------------------------

    def updateGratingPosition(self, newPosition):
        
        self.gratingPosition.config(text = "Angstroms from  zero order: " + str(newPosition))
        
#--------------------------------------------------------------------------------------------------

    def updateMotorsPositions(self, axisNum):
        
        if (axisNum == 1):
            self.rButton1.config(text = ("Motor 1 - Position: " + str(self.OmsLib.getMotorAxisPosition(1))))
            
        elif (axisNum == 2):
            self.rButton2.config(text = ("Motor 2 - Position: " + str(self.OmsLib.getMotorAxisPosition(2))))
            
        elif (axisNum == 3):
            self.rButton3.config(text = ("Motor 3 - Position: " + str(self.OmsLib.getMotorAxisPosition(3))))
            
        elif (axisNum == 4):
            self.rButton4.config(text = ("Motor 4 - Position: " + str(self.OmsLib.getMotorAxisPosition(4))))
            
        elif (axisNum == 6):
            self.rButton6.config(text = ("Motor 6 - Position: " + str(self.OmsLib.getMotorAxisPosition(6))))
            
        elif (axisNum == 7):
            self.rButton7.config(text = ("Motor 7 - Position: " + str(self.OmsLib.getMotorAxisPosition(7))))
        
#--------------------------------------------------------------------------------------------------

    #   Function to enable set button after it has been homed
    def gratingButtonToggle(self):
        
        self.gratingButton["state"] = "normal"
            
#--------------------------------------------------------------------------------------------------

################################################################################################################################
################################################################################################################################
################################################################################################################################

#   OMS CONTROLLER OBJECT, INHERITS GUI OBJECT
class Oms(object):

    def __init__(self, gui):

        #----VARIALBES----------------------------------------------------------

        #   Gui object
        self.gui = gui
        #   OMS library
        self.lib = ct.WinDLL("./Important_Files/MAXkSoftware/MAXkWebsiteWindows10/lib/Win10/x64/OmsMAXkMC.dll")
        print("lib: ", self.lib)
        #   Create mutatable character buffer, returns c_char. h is a list, pt is c_types.c_char_p
        h = [ct.create_string_buffer(b"OmsMAXk1")]
        #----------------------------------------------------------------------
        #   pt declares itself as c_char_p variable
        #   * allows for variable number of arguments to be passed
        #   map() loops through function ct.addressof with h being  only iterable
        #   ct.addressof() returns address of h as an int
        #----------------------------------------------------------------------
        pt = (ct.c_char_p)(*map(ct.addressof, h))
        #   Controller handle
        self.handle = self.lib.GetOmsHandle(pt)
        print("handle: ", self.handle)
        #   Controller log
        self.log = ""
        #   OMS controller model
        self.model = self.getModel()
        #   True or false value determining if drivers were loaded
        self.libConnection = self.checkLibrary()
        #   Grating position in angstroms
        self.gratingAngstromPosition = int()

#--------------------------------------------------------------------------------------------------
#----------------------------------GETTERS---------------------------------------------------------
#--------------------------------------------------------------------------------------------------
       
    def getModel(self):
        
        if (self.handle  == 0):
            model = "No controller detected"
            return model

        self.addLog("Attempting to retrieve model...")

        #   MODEL VARIABLE DECLARED AS A C STRING BUFFER
        model = ct.create_string_buffer(80)
        
        retVal = int()
        c_retVal = ct.c_long(retVal)
        
        c_retVal = self.lib.GetOmsControllerDescription( self.handle, model)
        
        self.handleReturnValue(c_retVal)
        
        retModel = model.value
        
        return retModel
    
#--------------------------------------------------------------------------------------------------

    def getLog(self):

        return self.log

#--------------------------------------------------------------------------------------------------
            
    def getMotorAxisPosition(self, axis):
        
        self.addLog("Attempting to retrieve axis #" + str(axis) + " position...")
        
        #   Determine axis is being called
        axisAsInt = self.determineAxisAsInt(axis)
        
        c_axis = ct.c_long(axisAsInt)
        
        position = int()
        c_position = ct.c_long(position)
        
        retVal = int()
        c_retVal = ct.c_long(retVal)
        
        #----------------------------------------------------------------------------------------------
        #   ct.byref creates a psuedo-pointer to the object passed in as an argument,
        #   in this case it creates a "pointer" to a long, which GetOmsAxisMotorPosition uses to fill-in
        #   the underlying long with the motor position 
        #----------------------------------------------------------------------------------------------
        c_retVal = self.lib.GetOmsAxisMotorPosition(self.handle, c_axis, ct.byref(c_position))
        
        #   ERROR HANDLING
        self.handleReturnValue(c_retVal)
        
        position = c_position.value
        
        return position
            
#--------------------------------------------------------------------------------------------------
        
    def getAxisVelocity(self, axis):
        
        self.addLog("Attempting to retrieve velocity for motor #" + str(axis))
        
        axisAsInt = self.determineAxisAsInt(axis)
        
        c_axis = ct.c_long(axisAsInt)
        
        velocity = int()
        c_velocity = ct.c_long(velocity)
        
        retVal = int()
        c_retVal = ct.c_long(retVal)
        
        c_retVal = self.lib.GetOmsAxisVelocity(self.handle, c_axis, c_velocity)
        
        self.handleReturnValue(c_retVal)
        
        velocity = c_velocity.value
        
        self.addLog("Motor velocity set to: " + str(velocity))
        
#--------------------------------------------------------------------------------------------------
        
    def getAxisAcceleration(self, axis):
        
        self.addLog("Attempting to retrieve acceleration for motor #" + str(axis))

        axisAsInt = self.determineAxisAsInt(axis)
        c_axis = ct.c_long(axisAsInt)
        
        acceleration = int()
        c_acceleration = ct.c_long(acceleration)
        
        retVal = int()
        c_retVal = ct.c_long(retVal)
        
        c_retVal = self.lib.GetOmsAxisAcceleration(self.handle, c_axis, c_acceleration)
        
        self.handleReturnValue(c_retVal)
        
        acceleration = c_acceleration.value
        
        self.addLog("Motor acceleration set to: " + str(acceleration))
        
#--------------------------------------------------------------------------------------------------

    def getGratingPosition(self):
        
        return self.gratingAngstromPosition
 
#--------------------------------------------------------------------------------------------------
#--------------------------------------SETTERS-----------------------------------------------------
#--------------------------------------------------------------------------------------------------
        
    def setAxisBaseVelocity(self, axis, velocity):
        
        self.addLog("Attempting to set axis #" + str(axis) + " base velocity...")
        
        #   Determine which axis is being called
        axisAsInt = self.determineAxisAsInt(axis)
        
        c_axis = ct.c_long(axisAsInt)
        c_velocity = ct.c_long(velocity)
        

        #   Check to see if base velocity input is less than max velocity
        velocityCheck = int()
        c_velocityCheck = ct.c_long(velocityCheck)
        
        self.lib.GetOmsAxisVelocity(self.handle, c_axis, c_velocityCheck)
        
        velocityCheck = c_velocityCheck.value
        
        if(velocity < velocityCheck):
            self.addLog("Base velocity must be less than max velocity")
            self.addLog("Max velocity currently set to: " + velocityCheck)
            return
            
        retVal = int()
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
        
        retVal = int()
        c_retVal = ct.c_long(retVal)
        c_retVal = self.lib.SetOmsAxisVelocity(self.handle, c_axis, c_velocity)
        
        #   ERROR HANDLING
        self.handleReturnValue(c_retVal)
        
#--------------------------------------------------------------------------------------------------
            
    def setAxisAcceleration(self, axis, acceleration):
              
        self.addLog("Attempting to set axis #" + str(axis) + " acceleration...")
        
        if (acceleration < 1 or acceleration > 8000000):
            self.addLog("Value must be between 1 - 8,000,000")
            return
            
            
        #   Determine which axis is being called
        axisAsInt = self.determineAxisAsInt(axis)
        
        c_axis = ct.c_long(axisAsInt)
        c_acceleration = ct.c_long(acceleration)
            
        retVal = int()
        c_retVal = ct.c_long(retVal)
        c_retVal = self.lib.SetOmsAxisAcceleration(self.handle, c_axis, c_acceleration)
            
        #   ERROR HANDLING
        self.handleReturnValue(c_retVal)
            
#--------------------------------------------------------------------------------------------------

    def setInitalMotorPosition(self, axis, position):
        
        self.log("Setting motor #" + str(axis) + " to postion: " + str(position))
        
        axisAsInt = self.determineAxisAsInt(axis)
        c_axis = ct.c_long(axisAsInt)
        
        c_position = ct.c_long(position)
        
        retVal = int()
        c_retVal = ct.c_long(retVal)
        
        c_retVal = self.lib.SetOmsAxisPosition(self.handle, c_axis, c_position)
        
        self.handleReturnValue(c_retVal)
        
#--------------------------------------------------------------------------------------------------

    def setMCPGateValveIOBit(self, state):
            
        if (self.handle == 0):
            self.addLog("ERRROR: OMS handle invalid")
            return
            
        #OMS_LIB.SetOmsIOBit(OMS_HANDLE, 3, state)
        #time.sleep(GATE_VALVE_SLEEP_TIME)
            
        retVal = int()
        c_retVal = ct.c_long(retVal)
            
        c_state = ct.c_long(state)
        c_retVal = self.lib.SetOmsIOBit(self.handle, ct.c_long(3), c_state)
            
        self.handleReturnValue(c_retVal)
            
#--------------------------------------------------------------------------------------------------
#----------------------------------OTHER FUNCTIONS-------------------------------------------------
#--------------------------------------------------------------------------------------------------

    def checkLibrary(self):
        
        #   Checking to see if drivers are loaded
        if(self.handle == 0):
            self.addLog("-Driver for device was not loaded.")
            return False
        
        self.addLog("-Drivers loaded successfully")
        return True

#--------------------------------------------------------------------------------------------------

    def addLog(self, arg):

        self.log = self.getLog() + str(arg) + "\n"
        
#--------------------------------------------------------------------------------------------------

    def resetController(self):
        
        self.addLog("Attempting to reset controller...")
        
        retVal = int()
        c_retVal = ct.c_long(retVal)

        c_retVal = self.lib.ResetOmsController(self.handle)

        #   Logs reset status
        self.handleReturnValue(c_retVal)

#--------------------------------------------------------------------------------------------------

    def closeHandle(self):
        
        self.lib.CloseOmsHandle(self.handle)
            
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
        
        retVal = int()
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

    def moveGrating(self, angstromToSet):
        
        self.addLog("Attempting to move the grating to " + str(angstromToSet) + " angstroms")
        
        stepsPerTick = 255.9613
        const = 0.9932
        
        currentPosition = self.gratingAngstromPosition
        
        angstromDifference = angstromToSet - currentPosition
        
        motorStepSize = int((angstromDifference * const) * stepsPerTick)
        
        self.moveOmsAxisRelativeWait(5, motorStepSize)
        
        self.gratingAngstromPosition = angstromToSet
    
#--------------------------------------------------------------------------------------------------

    def homeGrating(self):
        
        self.addLog("Homing the grating to zero order...")
        
        #   Position of zero-order on the analog step reader
        zeroOrder = 10947
        #   Position of the lower limit switch
        lowerLim = 5885
        #   Number of motor steps that will move the analog reader 1 tick
        stepsPerTick = 255.9613
        
        velocity = 4000
        c_velocity = ct.c_long(velocity * 2)
        
        #motorAxis = 0x0010
        axis = self.determineAxisAsInt(5)
        c_axis = ct.c_long(axis)
        
        timeLim = 300000
        c_timeLim = ct.c_long(timeLim)
        
        retVal = int()
        c_retVal = ct.c_long(retVal)
        
        #   Sets axis limit logic
        self.lib.ConfigureOmsAxisLimitInput(self.handle, c_axis, 1)
        
        #   "Home" grating motor - goto lower limit, then travel to zero order
        self.lib.FindOmsAxisRevLimit(self.handle, c_axis, c_velocity, c_timeLim)
        calcZeroOrder = math.floor((zeroOrder - lowerLim) * stepsPerTick)
        c_calcZeroOrder = ct.c_long(calcZeroOrder)
        #   Moving the grating
        c_retVal = self.lib.MoveOmsAxisRelWait(self.handle, c_axis, c_calcZeroOrder, c_timeLim)
        
        self.gratingAngstromPosition = 0
        
        self.handleReturnValue(c_retVal)
        
#--------------------------------------------------------------------------------------------------
        
    def openMCPGate(self):
            
        self.addLog("Opening MCP Gate Valve")
            
        self.setMCPGateValveIOBit(1)  
        
#--------------------------------------------------------------------------------------------------

    def closeMCPGate(self):
            
        self.addLog("Closing MCP Gate Valve")
            
        self.setMCPGateValveIOBit(0)
        
#--------------------------------------------------------------------------------------------------

    def saveLog(self):
        
        print("Saving log before end of program")
        
        localTime = time.asctime(time.localtime(time.time()))
        
        saveFile = open("EuvLog.txt", "a")
        saveFile.write(str(localTime) + "\n" + self.getLog() + "\n" + "\n")
        
#--------------------------------------------------------------------------------------------------
        
################################################################################################################################
################################################################################################################################
################################################################################################################################

def main():

    #   GUI object
    EUV = EUVGUI()

    #   Run GUI main loop
    EUV.root.mainloop()
    
    #   Close handle
    EUV.OmsLib.closeHandle()
    
    #   Save log
    EUV.OmsLib.saveLog()
   
    print("End of program")

#--------------------------------------------------------------------------------------------------

#DRIVER CODE

if __name__ == '__main__' :

    main()
    
#--------------------------------------------------------------------------------------------------