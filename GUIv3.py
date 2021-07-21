# -*- coding: utf-8 -*-

"""

Created on Mon Aug 31 11:15:46 2020

 

@author: Earthman

"""

 

import ctypes as ct
import tkinter as tk


#GUI OBJECT

class EUVGUI(object):

    def __init__(self):

        #GLOBAL VARIABLES

        #GUI Window
        self.root = tk.Tk()
        self.root.title("EUV Graphical User Interface")

        #C Library Object
        self.OmsLib = Oms(self)
        #Log
        self.guiLog = self.OmsLib.log


        #GUI VARIABLES
        #Padding
        self.root['padx'] = 5
        self.root['pady'] = 5
        #String for commands that will be sent
        self.commandSend = ""
       
        #CREATE WIDGETS

        #Purple Dot
        self.purpleDotParent = tk.Canvas(height = 50, width = 50)
        self.purpleDot = self.purpleDotParent.create_oval(2, 2, 48, 48, fill = "MediumPurple")
        self.purpleDotParent.grid(row = 0, column = 0)

        #GUI Label
        self.title = tk.Label(text = "EUV GUI")
        self.title.grid(row = 0, column = 1)

        #Controller Model
        self.modelLabel = tk.Label(text = "Controller Model: " + str(self.OmsLib.model.value))
        self.modelLabel.grid(row = 0, column = 2)

        #Send Command Frame
        self.commandFrame = tk.LabelFrame(self.root, text = "Send command to controller:", relief = "ridge")
        self.commandFrame.grid(row = 0, column = 3)
        #Entry
        self.command = tk.Entry(self.commandFrame, width = 10)
        self.command.grid(row = 0, column = 0)
        #Button
        self.commandButton = tk.Button(self.commandFrame, text = "Send", command = lambda : [self.OmsLib.sendCommand(str(self.command.get())), self.updateLog()])
        self.commandButton.grid(row = 1, column = 0)

        #Reset Button. Updates the log regarding if reset was successful or not
        self.resetButton = tk.Button(text = "Reset Controller", command = lambda : [self.OmsLib.resetController(), self.updateLog()])
        self.resetButton.grid(row = 0, column = 4)

        #Controller Log. Prints what controller is doing
        self.logLabel = tk.Label(text = "Controller Log: \n" + self.guiLog, relief = "ridge")
        self.logLabel.grid(row = 1, column = 1, rowspan = 10)
        
        
        ## MOTOR 1 ################################################################################################
        ############################################################################################################
        #   Frame
        self.motor1Frame = tk.LabelFrame(self.root, text = "Motor #1", relief = "ridge")
        self.motor1Frame.grid(row = 1, column = 3)
        
        #   Motor position
        self.motor1Pos = tk.Label(self.motor1Frame, text = ("Axis #1 motor position: " + str(self.OmsLib.getMotorAxisPosition("1"))))
        self.motor1Pos.grid(row = 0, column = 1)
        
        #   Motor commands
        self.motor1Label = tk.Label(self.motor1Frame, text = "Enter number of steps to move relative to its position:")
        self.motor1Label.grid(row = 1, column = 0)
        #   Entry
        self.motor1Entry = tk.Entry(self.motor1Frame, width = 10)
        self.motor1Entry.grid(row = 2, column = 0)
        #   Send button
        self.motor1Button = tk.Button(self.motor1Frame, text = "Send", command = lambda : [self.OmsLib.moveOmsAxisRelativeWait(1, int(self.motor1Entry.get())), self.updateLog()])
        self.motor1Button.grid(row = 3, column = 0)
        
        #   Base veloctiy controls
        self.baseVelocityLabel = tk.Label(self.motor1Frame, text = "Set base velocity:")
        self.baseVelocityLabel.grid(row = 1, column = 1)
        #   Entry
        self.baseVelocityEntry = tk.Entry(self.motor1Frame, width = 10)
        self.baseVelocityEntry.grid(row = 2, column = 1)
        #   Button
        self.baseVelocityButton = tk.Button(self.motor1Frame, text = "Set", command = lambda : [self.OmsLib.setAxisBaseVelocity(1, int(self.baseVelocityEntry.get())), self.updateLog()])
        self.baseVelocityButton.grid(row = 3, column = 1)
        
        #   Velocity control options
        self.velocityLabel = tk.Label(self.motor1Frame, text = "Set velocity:")
        self.velocityLabel.grid(row = 1, column = 2)
        #   Entry
        self.velocityEntry = tk.Entry(self.motor1Frame, width = 10)
        self.velocityEntry.grid(row = 2, column = 2)
        #   Button
        self.velocityButton = tk.Button(self.motor1Frame, text = "Set", command = lambda : [self.OmsLib.setAxisVelocity(1, int(self.velocityEntry.get())), self.updateLog()])
        self.velocityButton.grid(row = 3, column = 2)
        
        #   Acceleration control options
        self.accelerationLabel = tk.Label(self.motor1Frame, text = "Set acceleration:")
        self.accelerationLabel.grid(row = 1, column = 3)
        #   Entry
        self.accelerationEntry = tk.Entry(self.motor1Frame, width = 10)
        self.accelerationEntry.grid(row = 2, column = 3)
        #   Button
        self.accelerationButton = tk.Button(self.motor1Frame, text = "Set", command = lambda : [self.OmsLib.setAxisAcceleration(1, int(self.accelerationEntry.get())), self.updateLog()])
        self.accelerationButton.grid(row = 3, column = 3)
        
        ############################################################################################################
        
        
        ### MOTOR #2 ################################################################################################
        ############################################################################################################
        #   Frame
        self.motor2Frame = tk.LabelFrame(self.root, text = "Motor #2", relief = "ridge")
        self.motor2Frame.grid(row = 2, column = 3)
        
        #   Motor position
        self.motor2Pos = tk.Label(self.motor2Frame, text = ("Axis #2 motor position: " + str(self.OmsLib.getMotorAxisPosition("2"))))
        self.motor2Pos.grid(row = 0, column = 1)
        
        #   Motor commands
        self.motor2Label = tk.Label(self.motor2Frame, text = "Enter number of steps to move relative to its position:")
        self.motor2Label.grid(row = 1, column = 0)
        #   Entry
        self.motor2Entry = tk.Entry(self.motor2Frame, width = 10)
        self.motor2Entry.grid(row = 2, column = 0)
        #   Send button
        self.motor2Button = tk.Button(self.motor2Frame, text = "Send", command = lambda : [self.OmsLib.moveOmsAxisRelativeWait(2, int(self.motor2Entry.get())), self.updateLog()])
        self.motor2Button.grid(row = 3, column = 0)
        
        #   Base veloctiy controls
        self.baseVelocityLabel2 = tk.Label(self.motor2Frame, text = "Set base velocity:")
        self.baseVelocityLabel2.grid(row = 1, column = 1)
        #   Entry
        self.baseVelocityEntry2 = tk.Entry(self.motor2Frame, width = 10)
        self.baseVelocityEntry2.grid(row = 2, column = 1)
        #   Button
        self.baseVelocityButton2 = tk.Button(self.motor2Frame, text = "Set", command = lambda : [self.OmsLib.setAxisBaseVelocity(2, int(self.baseVelocityEntry2.get())), self.updateLog()])
        self.baseVelocityButton2.grid(row = 3, column = 1)
        
        #   Velocity control options
        self.velocityLabel2 = tk.Label(self.motor2Frame, text = "Set velocity:")
        self.velocityLabel2.grid(row = 1, column = 2)
        #Entry
        self.velocityEntry2 = tk.Entry(self.motor2Frame, width = 10)
        self.velocityEntry2.grid(row = 2, column = 2)
        #   Button
        self.velocityButton2 = tk.Button(self.motor2Frame, text = "Set", command = lambda : [self.OmsLib.setAxisVelocity(2, int(self.velocityEntry2.get())), self.updateLog()])
        self.velocityButton2.grid(row = 3, column = 2)
        
        #   Acceleration control options
        self.accelerationLabel2 = tk.Label(self.motor2Frame, text = "Set acceleration:")
        self.accelerationLabel2.grid(row = 1, column = 3)
        #   Entry
        self.accelerationEntry2 = tk.Entry(self.motor2Frame, width = 10)
        self.accelerationEntry2.grid(row = 2, column = 3)
        #   Button
        self.accelerationButton2 = tk.Button(self.motor2Frame, text = "Set", command = lambda : [self.OmsLib.setAxisAcceleration(2, int(self.accelerationEntry2.get())), self.updateLog()])
        self.accelerationButton2.grid(row = 3, column = 3)
        
        ############################################################################################################
        
        
        ## MOTOR 3 ################################################################################################
        ############################################################################################################
        #   Frame
        self.motor3Frame = tk.LabelFrame(self.root, text = "Motor #3", relief = "ridge")
        self.motor3Frame.grid(row = 3, column = 3)
        
        #   Motor position
        self.motor3Pos = tk.Label(self.motor3Frame, text = ("Axis #3 motor position: " + str(self.OmsLib.getMotorAxisPosition("3"))))
        self.motor3Pos.grid(row = 0, column = 1)
        
        #   Motor commands
        self.motor3Label = tk.Label(self.motor3Frame, text = "Enter number of steps to move relative to its position:")
        self.motor3Label.grid(row = 1, column = 0)
        #   Entry
        self.motor3Entry = tk.Entry(self.motor3Frame, width = 10)
        self.motor3Entry.grid(row = 2, column = 0)
        #   Send button
        self.motor3Button = tk.Button(self.motor3Frame, text = "Send", command = lambda : [self.OmsLib.moveOmsAxisRelativeWait(3, int(self.motor3Entry.get())), self.updateLog()])
        self.motor3Button.grid(row = 3, column = 0)
        
        #   Base veloctiy controls
        self.baseVelocityLabel3 = tk.Label(self.motor3Frame, text = "Set base velocity:")
        self.baseVelocityLabel3.grid(row = 1, column = 1)
        #   Entry
        self.baseVelocityEntry3 = tk.Entry(self.motor3Frame, width = 10)
        self.baseVelocityEntry3.grid(row = 2, column = 1)
        #   Button
        self.baseVelocityButton3 = tk.Button(self.motor3Frame, text = "Set", command = lambda : [self.OmsLib.setAxisBaseVelocity(3, int(self.baseVelocityEntry3.get())), self.updateLog()])
        self.baseVelocityButton3.grid(row = 3, column = 1)
        
        #   Velocity control options
        self.velocityLabel3 = tk.Label(self.motor3Frame, text = "Set velocity:")
        self.velocityLabel3.grid(row = 1, column = 2)
        #   Entry
        self.velocityEntry3 = tk.Entry(self.motor3Frame, width = 10)
        self.velocityEntry3.grid(row = 2, column = 2)
        #   Button
        self.velocityButton3 = tk.Button(self.motor3Frame, text = "Set", command = lambda : [self.OmsLib.setAxisVelocity(3, int(self.velocityEntry3.get())), self.updateLog()])
        self.velocityButton3.grid(row = 3, column = 2)
        
        #   Acceleration control options
        self.accelerationLabel3 = tk.Label(self.motor3Frame, text = "Set acceleration:")
        self.accelerationLabel3.grid(row = 1, column = 3)
        #   Entry
        self.accelerationEntry3 = tk.Entry(self.motor3Frame, width = 10)
        self.accelerationEntry3.grid(row = 2, column = 3)
        #   Button
        self.accelerationButton3 = tk.Button(self.motor3Frame, text = "Set", command = lambda : [self.OmsLib.setAxisAcceleration(3, int(self.accelerationEntry3.get())), self.updateLog()])
        self.accelerationButton3.grid(row = 3, column = 3)
        
        ############################################################################################################
        
        
        ### MOTOR 4 ################################################################################################
        ############################################################################################################
        #   Frame
        self.motor4Frame = tk.LabelFrame(self.root, text = "Motor #4", relief = "ridge")
        self.motor4Frame.grid(row = 4, column = 3)
        
        #   Motor position
        self.motor4Pos = tk.Label(self.motor4Frame, text = ("Axis #4 motor position: " + str(self.OmsLib.getMotorAxisPosition("4"))))
        self.motor4Pos.grid(row = 0, column = 1)
        
        #   Motor commands
        self.motor4Label = tk.Label(self.motor4Frame, text = "Enter number of steps to move relative to its position:")
        self.motor4Label.grid(row = 1, column = 0)
        #   Entry
        self.motor4Entry = tk.Entry(self.motor4Frame, width = 10)
        self.motor4Entry.grid(row = 2, column = 0)
        #   Send button
        self.motor4Button = tk.Button(self.motor4Frame, text = "Send", command = lambda : [self.OmsLib.moveOmsAxisRelativeWait(4, int(self.motor4Entry.get())), self.updateLog()])
        self.motor4Button.grid(row = 3, column = 0)
        
        #   Base veloctiy controls
        self.baseVelocityLabel4 = tk.Label(self.motor4Frame, text = "Set base velocity:")
        self.baseVelocityLabel4.grid(row = 1, column = 1)
        #   Entry
        self.baseVelocityEntry4 = tk.Entry(self.motor4Frame, width = 10)
        self.baseVelocityEntry4.grid(row = 2, column = 1)
        #   Button
        self.baseVelocityButton4 = tk.Button(self.motor4Frame, text = "Set", command = lambda : [self.OmsLib.setAxisBaseVelocity(4, int(self.baseVelocityEntry4.get())), self.updateLog()])
        self.baseVelocityButton4.grid(row = 3, column = 1)
        
        #   Velocity control options
        self.velocityLabel4 = tk.Label(self.motor4Frame, text = "Set velocity:")
        self.velocityLabel4.grid(row = 1, column = 2)
        #   Entry
        self.velocityEntry4 = tk.Entry(self.motor4Frame, width = 10)
        self.velocityEntry4.grid(row = 2, column = 2)
        #   Button
        self.velocityButton4 = tk.Button(self.motor4Frame, text = "Set", command = lambda : [self.OmsLib.setAxisVelocity(4, int(self.velocityEntry4.get())), self.updateLog()])
        self.velocityButton4.grid(row = 3, column = 2)
        
        #   Acceleration control options
        self.accelerationLabel4 = tk.Label(self.motor4Frame, text = "Set acceleration:")
        self.accelerationLabel4.grid(row = 1, column = 3)
        #   Entry
        self.accelerationEntry4 = tk.Entry(self.motor4Frame, width = 10)
        self.accelerationEntry4.grid(row = 2, column = 3)
        #   Button
        self.accelerationButton4 = tk.Button(self.motor4Frame, text = "Set", command = lambda : [self.OmsLib.setAxisAcceleration(4, int(self.accelerationEntry4.get())), self.updateLog()])
        self.accelerationButton4.grid(row = 3, column = 3)
        
        ############################################################################################################
        
        
        ### MOTOR 5 ################################################################################################
        ############################################################################################################
        #   Frame
        self.motor5Frame = tk.LabelFrame(self.root, text = "Motor #5", relief = "ridge")
        self.motor5Frame.grid(row = 5, column = 3)
        
        #   Motor position
        self.motor5Pos = tk.Label(self.motor5Frame, text = ("Axis #5 motor position: " + str(self.OmsLib.getMotorAxisPosition("5"))))
        self.motor5Pos.grid(row = 0, column = 1)
        
        #   Motor commands
        self.motor5Label = tk.Label(self.motor5Frame, text = "Enter number of steps to move relative to its position:")
        self.motor5Label.grid(row = 1, column = 0)
        #   Entry
        self.motor5Entry = tk.Entry(self.motor5Frame, width = 10)
        self.motor5Entry.grid(row = 2, column = 0)
        #   Send button
        self.motor5Button = tk.Button(self.motor5Frame, text = "Send", command = lambda : [self.OmsLib.moveOmsAxisRelativeWait(5, int(self.motor5Entry.get())), self.updateLog()])
        self.motor5Button.grid(row = 3, column = 0)
        
        #   Base veloctiy controls
        self.baseVelocityLabel5 = tk.Label(self.motor5Frame, text = "Set base velocity:")
        self.baseVelocityLabel5.grid(row = 1, column = 1)
        #   Entry
        self.baseVelocityEntry5 = tk.Entry(self.motor5Frame, width = 10)
        self.baseVelocityEntry5.grid(row = 2, column = 1)
        #   Button
        self.baseVelocityButton5 = tk.Button(self.motor5Frame, text = "Set", command = lambda : [self.OmsLib.setAxisBaseVelocity(5, int(self.baseVelocityEntry5.get())), self.updateLog()])
        self.baseVelocityButton5.grid(row = 3, column = 1)
        
        #   Velocity control options
        self.velocityLabel5 = tk.Label(self.motor5Frame, text = "Set velocity:")
        self.velocityLabel5.grid(row = 1, column = 2)
        #   Entry
        self.velocityEntry5 = tk.Entry(self.motor5Frame, width = 10)
        self.velocityEntry5.grid(row = 2, column = 2)
        #   Button
        self.velocityButton5 = tk.Button(self.motor5Frame, text = "Set", command = lambda : [self.OmsLib.setAxisVelocity(5, int(self.velocityEntry5.get())), self.updateLog()])
        self.velocityButton5.grid(row = 3, column = 2)
        
        #   Acceleration control options
        self.accelerationLabel5 = tk.Label(self.motor5Frame, text = "Set acceleration:")
        self.accelerationLabel5.grid(row = 1, column = 3)
        #   Entry
        self.accelerationEntry5 = tk.Entry(self.motor5Frame, width = 10)
        self.accelerationEntry5.grid(row = 2, column = 3)
        #   Button
        self.accelerationButton5 = tk.Button(self.motor5Frame, text = "Set", command = lambda : [self.OmsLib.setAxisAcceleration(5, int(self.accelerationEntry5.get())), self.updateLog()])
        self.accelerationButton5.grid(row = 3, column = 3)
        
        ############################################################################################################
        
        
        ### MOTOR 6 ################################################################################################
        ############################################################################################################
        #   Frame
        self.motor6Frame = tk.LabelFrame(self.root, text = "Motor #6", relief = "ridge")
        self.motor6Frame.grid(row = 6, column = 3)
        
        #   Motor position
        self.motor6Pos = tk.Label(self.motor6Frame, text = ("Axis #6 motor position: " + str(self.OmsLib.getMotorAxisPosition("6"))))
        self.motor6Pos.grid(row = 0, column = 1)
        
        #   Motor commands
        self.motor6Label = tk.Label(self.motor6Frame, text = "Enter number of steps to move relative to its position:")
        self.motor6Label.grid(row = 1, column = 0)
        #   Entry
        self.motor6Entry = tk.Entry(self.motor6Frame, width = 10)
        self.motor6Entry.grid(row = 2, column = 0)
        #   Send button
        self.motor6Button = tk.Button(self.motor6Frame, text = "Send", command = lambda : [self.OmsLib.moveOmsAxisRelativeWait(6, int(self.motor6Entry.get())), self.updateLog()])
        self.motor6Button.grid(row = 3, column = 0)
        
        #   Base veloctiy controls
        self.baseVelocityLabel6 = tk.Label(self.motor6Frame, text = "Set base velocity:")
        self.baseVelocityLabel6.grid(row = 1, column = 1)
        #   Entry
        self.baseVelocityEntry6 = tk.Entry(self.motor6Frame, width = 10)
        self.baseVelocityEntry6.grid(row = 2, column = 1)
        #   Button
        self.baseVelocityButton6 = tk.Button(self.motor6Frame, text = "Set", command = lambda : [self.OmsLib.setAxisBaseVelocity(6, int(self.baseVelocityEntry6.get())), self.updateLog()])
        self.baseVelocityButton6.grid(row = 3, column = 1)
        
        #   Velocity control options
        self.velocityLabel6 = tk.Label(self.motor6Frame, text = "Set velocity:")
        self.velocityLabel6.grid(row = 1, column = 2)
        #   Entry
        self.velocityEntry6 = tk.Entry(self.motor6Frame, width = 10)
        self.velocityEntry6.grid(row = 2, column = 2)
        #   Button
        self.velocityButton6 = tk.Button(self.motor6Frame, text = "Set", command = lambda : [self.OmsLib.setAxisVelocity(6, int(self.velocityEntry6.get())), self.updateLog()])
        self.velocityButton6.grid(row = 3, column = 2)
        
        #   Acceleration control options
        self.accelerationLabel6 = tk.Label(self.motor6Frame, text = "Set acceleration:")
        self.accelerationLabel6.grid(row = 1, column = 3)
        #   Entry
        self.accelerationEntry6 = tk.Entry(self.motor6Frame, width = 10)
        self.accelerationEntry6.grid(row = 2, column = 3)
        #   Button
        self.accelerationButton6 = tk.Button(self.motor6Frame, text = "Set", command = lambda : [self.OmsLib.setAxisAcceleration(6, int(self.accelerationEntry6.get())), self.updateLog()])
        self.accelerationButton6.grid(row = 3, column = 3)
        
        ############################################################################################################
        
        
        ### MOTOR 7 ################################################################################################
        ############################################################################################################
        #   Frame
        self.motor7Frame = tk.LabelFrame(self.root, text = "Motor #7", relief = "ridge")
        self.motor7Frame.grid(row = 7, column = 3)
        
        #   Motor position
        self.motor7Pos = tk.Label(self.motor7Frame, text = ("Axis #7 motor position: " + str(self.OmsLib.getMotorAxisPosition("7"))))
        self.motor7Pos.grid(row = 0, column = 1)
        
        #   Motor commands
        self.motor7Label = tk.Label(self.motor7Frame, text = "Enter number of steps to move relative to its position:")
        self.motor7Label.grid(row = 1, column = 0)
        #   Entry
        self.motor7Entry = tk.Entry(self.motor7Frame, width = 10)
        self.motor7Entry.grid(row = 2, column = 0)
        #   Send button
        self.motor7Button = tk.Button(self.motor7Frame, text = "Send", command = lambda : [self.OmsLib.moveOmsAxisRelativeWait(7, int(self.motor7Entry.get())), self.updateLog()])
        self.motor7Button.grid(row = 3, column = 0)
        
        #   Base veloctiy controls
        self.baseVelocityLabel7 = tk.Label(self.motor7Frame, text = "Set base velocity:")
        self.baseVelocityLabel7.grid(row = 1, column = 1)
        #   Entry
        self.baseVelocityEntry7 = tk.Entry(self.motor7Frame, width = 10)
        self.baseVelocityEntry7.grid(row = 2, column = 1)
        #   Button
        self.baseVelocityButton7 = tk.Button(self.motor7Frame, text = "Set", command = lambda : [self.OmsLib.setAxisBaseVelocity(7, int(self.baseVelocityEntry7.get())), self.updateLog()])
        self.baseVelocityButton7.grid(row = 3, column = 1)
        
        #   Velocity control options
        self.velocityLabel7 = tk.Label(self.motor7Frame, text = "Set velocity:")
        self.velocityLabel7.grid(row = 1, column = 2)
        #   Entry
        self.velocityEntry7 = tk.Entry(self.motor7Frame, width = 10)
        self.velocityEntry7.grid(row = 2, column = 2)
        #   Button
        self.velocityButton7 = tk.Button(self.motor7Frame, text = "Set", command = lambda : [self.OmsLib.setAxisVelocity(7, int(self.velocityEntry7.get())), self.updateLog()])
        self.velocityButton7.grid(row = 3, column = 2)
        
        #   Acceleration control options
        self.accelerationLabel7 = tk.Label(self.motor7Frame, text = "Set acceleration:")
        self.accelerationLabel7.grid(row = 1, column = 3)
        #   Entry
        self.accelerationEntry7 = tk.Entry(self.motor7Frame, width = 10)
        self.accelerationEntry7.grid(row = 2, column = 3)
        #   Button
        self.accelerationButton7 = tk.Button(self.motor7Frame, text = "Set", command = lambda : [self.OmsLib.setAxisAcceleration(7, int(self.accelerationEntry7.get())), self.updateLog()])
        self.accelerationButton7.grid(row = 3, column = 3)
        
        ############################################################################################################
        
        #UPDATE LOG AT VERY END
        self.updateLog()


#--------------------------------------------------------------------------------------------------

    #GUI function to update the log on the screen
    def updateLog(self):

        self.logLabel.config(text = "Controller Log: \n" + self.OmsLib.getLog())
   

################################################################################################################################
################################################################################################################################
################################################################################################################################


#OMS CONTROLLER OBJECT, INHERITS GUI OBJECT
class Oms(object):

    def __init__(self, gui):

        #GLOBAL VARIABLES

        #GUI OBJECT
        self.gui = gui

        #OMS LIBRARY
        self.lib = ct.WinDLL("./Important_Files/MAXkSoftware/MAXkWebsiteWindows10/lib/Win10/x64/OmsMAXkMC.dll")
        print("lib: ", self.lib)
        
        #CREATE MUTATABLE CHARACTER BUFFER, RETURNS C_CHAR. h IS A LIST, pt IS CTYPES.C_CHAR_P
        h = [ct.create_string_buffer(b"OmsMAXk1")]
        
        ############################################################################################################
        #pt DECLARES ITSELF AS C_CHAR_P VARIABLE 
        # * ALLOWS FOR VARIABLE NUMBER OF ARGUMENTS TO BE PASSED
        #map() LOOPS THROUGH FUNCTION ct.addressof WITH h BEING ONLY INTERABLE.
        #ct.addressof() RETURNS ADDRESS OF h AS AN INT
        ############################################################################################################
        pt = (ct.c_char_p)(*map(ct.addressof, h))

        self.handle = self.lib.GetOmsHandle(pt)
        print("handle: ", self.handle)
        
        #CONTROLLER LOG
        self.log = "\n"

        #OMS CONTROLLER MODEL
        self.model = self.getModel()

        #TRUE OR FALSE VALUE DETERMINING IF DRIVERS WERE LOADED
        self.libConnection = self.checkLibrary()

       

#--------------------------------------------------------------------------------------------------

       
    #FUNCTION THAT SHOULD RETURN THE MODEL OF THE CONTROLLER
    def getModel(self):

        self.addLog("Attempting to retrieve model...")

        #MODEL VARIABLE DECLARED AS A C STRING BUFFER
        model = ct.create_string_buffer(80)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        
        c_retVal = self.lib.GetOmsControllerDescription( self.handle, model)
        
        self.handleReturnValue(c_retVal)
        

        return model


#--------------------------------------------------------------------------------------------------
        

    def checkLibrary(self):
        
        #Checking to see if drivers are loaded
        if(self.handle == 0):
            self.addLog("Driver for device was not loaded.")
            return False

        else:
            self.addLog("Drivers loaded successfully")
            return True


#--------------------------------------------------------------------------------------------------


    def sendCommand(self, arg):

        self.addLog("Attempting to send command: " + str(arg))
        
        returnStatus = 0
        c_returnStatus = ct.c_long(returnStatus)
        
        c_arg = ct.create_string_buffer(bytes(arg,'utf-8'))
        
        c_returnStatus = self.lib.SendString(self.handle, c_arg)

        self.handleReturnValue(c_returnStatus)

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

        #Logs reset status
        self.handleReturnValue(resetStatus)

           
#--------------------------------------------------------------------------------------------------


    def closeHandle(self):
        
        self.lib.CloseOmsHandle(self.handle)
        
        
#--------------------------------------------------------------------------------------------------
        
        
    def setAxisBaseVelocity(self, axis, velocity):
        
        self.addLog("Attempting to set axis #" + str(axis) + " base velocity...")
        
        self.axis = axis
        self.velocity = velocity
        
        #Determine which axis is being called
        axisAsInt = self.determineAxisAsInt(self.axis)
        
        c_axis = ct.c_long(axisAsInt)
        c_velocity = ct.c_long(self.velocity)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        
        c_retVal = self.lib.SetOmsAxisBaseVelocity(self.handle, c_axis, c_velocity)
        
        #ERROR HANDLING
        self.handleReturnValue(c_retVal)
            
            
#--------------------------------------------------------------------------------------------------
    
    def setAxisVelocity(self, axis, velocity):
        
        self.addLog("Attempting to set axis #" + str(axis) + " velocity...")
        
        self.axis = axis
        self.velocity = velocity
        
        #Determine which axis is being called
        axisAsInt = self.determineAxisAsInt(self.axis)
        
        c_axis = ct.c_long(axisAsInt)
        c_velocity = ct.c_long(self.velocity)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        c_retVal = self.lib.SetOmsAxisVelocity(self.handle, c_axis, c_velocity)
        
        
        #ERROR HANDLING
        self.handleReturnValue(c_retVal)
        
        
#--------------------------------------------------------------------------------------------------
            
    def setAxisAcceleration(self, axis, acceleration):
              
        self.addLog("Attempting to set axis #" + str(axis) + " acceleration...")
        
        self.axis = axis
        self.acceleration = acceleration
        
        #Determine which axis is being called
        axisAsInt = self.determineAxisAsInt(self.axis)
    
        c_axis = ct.c_long(axisAsInt)
        c_acceleration = ct.c_long(self.acceleration)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        c_retVal = self.lib.SetOmsAxisAcceleration(self.handle, c_axis, c_acceleration)
        
        
        #ERROR HANDLING
        self.handleReturnValue(c_retVal)
        
            
#--------------------------------------------------------------------------------------------------
            
    def getMotorAxisPosition(self, axis):
        
        self.addLog("Attempting to retrieve axis #" + str(axis) + " position...")
        
        #axis variable type is a string
        self.axis = axis
        
        #Determine which axis is being called
        axisAsInt = self.determineAxisAsInt(self.axis)
        
        c_axis = ct.c_long(axisAsInt)
        
        position = 0
        c_position = ct.c_long(position)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        
        ############################################################################################################
        # ct.byref creates a psuedo-pointer to the object passed in as an argument,
        # in this case it creates a "pointer" to a long, which GetOmsAxisMotorPosition uses to fill-in
        # the underlying long with the motor position 
        ############################################################################################################
        c_retVal = self.lib.GetOmsAxisMotorPosition(self.handle, c_axis, ct.byref(c_position))
        
        #ERROR HANDLING
        self.handleReturnValue(c_retVal)
        
        position = ct.c_long(position).value
        
        return position
            
#--------------------------------------------------------------------------------------------------
            
    def moveOmsAxisRelativeWait(self, axis, position):
        
        self.addLog("Attempting to move axis #" + str(axis) + " " + str(position) + " steps...")
        
        self.axis = axis
        self.position = position
        
        #Determine which axis is being called
        axisAsInt = self.determineAxisAsInt(self.axis)
        
        #Setting time limit so that it will wait 5 seconds before signaling time out, is measured in milliseconds
        timeLim = 5000
        c_timeLim = ct.c_long(timeLim)
        
        c_axis = ct.c_long(axisAsInt)
        #position variable is sent over as a string but needs to be an int to convert to long
        position = int(self.position)
        c_position = ct.c_long(position)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        
        c_retVal = self.lib.MoveOmsAxisRelWait(self.handle, c_axis, c_position, c_timeLim)
        
        
        #ERROR HANDLING
        self.handleReturnValue(c_retVal)

            
#--------------------------------------------------------------------------------------------------
            
    def handleReturnValue(self, returnValue):
        
        self.returnValue = returnValue
        
        if (self.returnValue == 0):
            self.addLog("Success")
            
        elif(self.returnValue == 1):
            self.addLog("Command time out")
            
        elif(self.returnValue == 2):
            self.addLog("Response time out")
        
        elif(self.returnValue == 3):
            self.addLog("Invalid axis selection")
        
        elif(self.returnValue == 4):
            self.addLog("Move time out")
            
        elif(self.returnValue == 5):
            self.addLog("Invalid parameter")
            
        elif(self.returnValue == 6):
            self.addLog("Invalid bit number")
            
        else:
            self.addLog("Value does not fall under OMS source code return values")
            
            
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


    #GUI object
    EUV = EUVGUI()

    #Run GUI main loop
    EUV.root.mainloop()
   
    print("End of program")


#--------------------------------------------------------------------------------------------------


#DRIVER CODE

if __name__ == '__main__' :

    main()
    
#--------------------------------------------------------------------------------------------------

