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


        #CREATE WIDGETS

        #GUI VARIABLES
        #Padding
        self.pad = 3
        #String for commands that will be sent
        self.commandSend = ""
       

        #Status light
        self.statusLightParent = tk.Canvas(height = 50, width = 50)
        self.statusLight = self.statusLightParent.create_oval(2, 2, 48, 48, fill = "MediumPurple")
        self.statusLightParent.grid(row = 0, column = 0, padx = self.pad, pady = self.pad)

        #GUI Label
        self.title = tk.Label(text = "EUV GUI")
        self.title.grid(row = 0, column = 1, columnspan = 2, padx = self.pad, pady = self.pad)

        #Controller Model
        self.modelLabel = tk.Label(text = "Controller Model: " + str(self.OmsLib.model.value))
        self.modelLabel.grid(row = 1, column = 2, padx = self.pad, pady = self.pad)

        #Command Label and Entry
        self.commandLabel = tk.Label(text = "Enter Command for the Controller:")
        self.commandLabel.grid(row = 3, column = 2, padx = self.pad, pady = self.pad)
        self.command = tk.Entry(width = 20)
        self.command.grid(row = 4, column = 2, padx = self.pad, pady = self.pad)

        #Send Command Button. After button is clicked, it sends command to Oms object and updates log
        #Command must be retrieved from Entry using .get() and needs to be converted to proper variable, haven't figured this out yet
        self.commandSend = self.command.get()
        self.commandButton = tk.Button(text = "Send", command = lambda :[self.OmsLib.sendCommand(self.command.get()), self.updateLog()])
        self.commandButton.grid(row = 5, column = 2, padx = self.pad, pady = self.pad)

        #Reset Button. Updates the log regarding if reset was successful or not
        self.resetButton = tk.Button(text = "Reset Controller", command = lambda : [self.OmsLib.resetController(), self.updateLog()])
        self.resetButton.grid(row = 1, column = 0, padx = self.pad, pady = self.pad)

        #Controller Log. Prints what controller is doing
        self.logLabel = tk.Label(text = "Controller Log: \n" + self.guiLog, relief = "ridge")
        self.logLabel.grid(row = 1, column = 1, rowspan = 10, padx = self.pad, pady = self.pad)
        
        
        #Axis 1 motor position
        self.motor1Pos = tk.Label(text = ("Axis 1 motor position: " + str(self.OmsLib.getMotorAxisPosition("1"))))
        self.motor1Pos.grid(row = 2, column = 2, padx = self.pad, pady = self.pad)
        #Axis 1 motor commands
        self.motor1Label = tk.Label(text = "Enter number of steps to move relative to its position:")
        self.motor1Label.grid(row = 2, column = 3, padx = self.pad, pady= self.pad)
        #Entry
        self.motor1Entry = tk.Entry(width = 20)
        self.motor1Entry.grid(row = 2, column = 4, padx = self.pad, pady = self.pad)
        #Send button
        self.motor1Button = tk.Button(text = "Send command to motor 1", command = lambda : [self.OmsLib.moveOmsAxisRelativeWait(1, int(self.motor1Entry.get())), self.updateLog()])
        self.motor1Button.grid(row = 2, column = 5, padx = self.pad, pady = self.pad)
        
        
        #Base veloctiy controls
        self.baseVelocityLabel = tk.Label(text = "Set base velocity:")
        self.baseVelocityLabel.grid(row = 3, column = 3, padx = self.pad, pady = self.pad)
        #Entry
        self.baseVelocityEntry = tk.Entry(width = 20)
        self.baseVelocityEntry.grid(row = 4, column = 3, padx = self.pad, pady = self.pad)
        #Send button
        self.baseVelocityButton = tk.Button(text = "Set base velocity", command = lambda : [self.OmsLib.setAxisBaseVelocity(1, int(self.baseVelocityEntry.get())), self.updateLog()])
        self.baseVelocityButton.grid(row = 5, column = 3, padx = self.pad, pady = self.pad)
        
        
        #Velocity control options
        self.velocityLabel = tk.Label(text = "Set velocity:")
        self.velocityLabel.grid(row = 3, column = 4, padx = self.pad, pady = self.pad)
        #Entry
        self.velocityEntry = tk.Entry(width = 20)
        self.velocityEntry.grid(row = 4, column = 4, padx = self.pad, pady = self.pad)
        #Send button
        self.velocityButton = tk.Button(text = "Set velocity", command = lambda : [self.OmsLib.setAxisVelocity(1, int(self.velocityEntry.get())), self.updateLog()])
        self.velocityButton.grid(row = 5, column = 4, padx = self.pad, pady = self.pad)
        
        
        #Acceleration control options
        self.accelerationLabel = tk.Label(text = "Set acceleration:")
        self.accelerationLabel.grid(row = 3, column = 5, padx = self.pad, pady = self.pad)
        #Entry
        self.accelerationEntry = tk.Entry(width = 20)
        self.accelerationEntry.grid(row = 4, column = 5, padx = self.pad, pady = self.pad)
        #Send button
        self.accelerationButton = tk.Button(text = "Set acceleration", command = lambda : [self.OmsLib.setAxisAcceleration(1, int(self.accelerationEntry.get())), self.updateLog()])
        self.accelerationButton.grid(row = 5, column = 5, padx = self.pad, pady = self.pad)
        
        
        #UPDATE LOG AT VERY END
        self.updateLog()


#--------------------------------------------------------------------------------------------------

    #GUI function to update the log on the screen
    def updateLog(self):

        self.logLabel.config(text = "Controller Log: \n" + self.OmsLib.getLog())
   

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
        #pt DECLARES ITSELF AS C_CHAR_P VARIABLE 
        # * ALLOWS FOR VARIABLE NUMBER OF ARGUMENTS TO BE PASSED
        #map() LOOPS THROUGH FUNCTION ct.addressof WITH h BEING ONLY INTERABLE.
        #ct.addressof() RETURNS ADDRESS OF h AS AN INT
        pt = (ct.c_char_p)(*map(ct.addressof, h))

        self.handle = self.lib.GetOmsHandle(pt)
        print("handle: ", self.handle)
        
        #CONTROLLER LOG
        self.log = ""

        #OMS CONTROLLER MODEL
        self.model = self.getModel()

        #TRUE OR FALSE VALUE DETERMINING IF DRIVERS WERE LOADED
        self.libConnection = self.checkLibrary()

       

#--------------------------------------------------------------------------------------------------

       
    #FUNCTION THAT SHOULD RETURN THE MODEL OF THE CONTROLLER
    def getModel(self):

     ## Fix me
        #model = ct.c_wchar_p("")

        self.addLog("Attempting to retrieve model...")

        #MODEL VARIABLE DECLARED AS A C STRING BUFFER
        model = ct.create_string_buffer(80)
        print("model: ", model.value)
        retVal = self.lib.GetOmsControllerDescription( self.handle, model)
        
        if (retVal != 0):
           print("Big Not Success: " + str(retVal))
            
        print("model: ", model.value)

        if(model.value == b""):
            self.addLog("Nothing was recieved")

        else:
            self.addLog("Obtained controller model")

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

        returnStatus = 0
        c_returnStatus = ct.c_long(returnStatus)
        
        c_arg = ct.create_string_buffer(bytes(arg,'utf-8'))
        
        c_returnStatus = self.lib.SendString(self.handle, c_arg)

        if(c_returnStatus == 1):
            self.addLog("Command timed out.")

        else:
            self.addLog("Command sent sucessfully")


#--------------------------------------------------------------------------------------------------


    def getLog(self):

        return self.log


#--------------------------------------------------------------------------------------------------


    def addLog(self, arg):

        self.log = self.getLog() + str(arg) + "\n"
        

#--------------------------------------------------------------------------------------------------


    def resetController(self):

        resetStatus = self.lib.ResetOmsController(self.handle)

        #Logs reset status
        if(resetStatus == 0):
            self.addLog("Reset Successful")
            
        elif(resetStatus == 1):
            self.addLog("Reset unsuccessful, command timed out.")

        else:
            self.addLog("Reset command returned unnatural value")

           
#--------------------------------------------------------------------------------------------------


    def closeHandle(self):
        
        self.lib.CloseOmsHandle(self.handle)
        
        
#--------------------------------------------------------------------------------------------------
        
        
    def setAxisBaseVelocity(self, axis, velocity):
        
        #axis and velocity are of variable type long
        #function returns a long
        c_axis = ct.c_long(axis)
        c_velocity = ct.c_long(velocity)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        
        c_retVal = self.lib.SetOmsAxisBaseVelocity(self.handle, c_axis, c_velocity)
        
        
        #ERROR HANDLING
        if(c_retVal == "SUCCESS"):
            self.addLog("Request was sent")
            
        elif(c_retVal == "COMMAND_TIME_OUT"):
            self.addLog("Command timed out")
            
        elif(c_retVal == "INVALID_AXIS_SELECTION"):
            self.addLog("Invalid axis value")
            
        elif(c_retVal == "INVALID PARAMETER"):
            self.addLog("Invalid velocity parameter")
            
            
#--------------------------------------------------------------------------------------------------
    
    def setAxisVelocity(self, axis, velocity):
        
        c_axis = ct.c_long(axis)
        c_velocity = ct.c_long(velocity)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        c_retVal = self.lib.SetOmsAxisVelocity(self.handle, c_axis, c_velocity)
        
        
        #ERROR HANDLING
        if(c_retVal == "SUCCESS"):
            self.addLog("Request was sent")
            
        elif(c_retVal == "COMMAND_TIME_OUT"):
            self.addLog("Command timed out")
            
        elif(c_retVal == "INVALID_AXIS_SELECTION"):
            self.addLog("Invalid axis value")
            
        elif(c_retVal == "INVALID PARAMETER"):
            self.addLog("Invalid velocity parameter")
        
        
#--------------------------------------------------------------------------------------------------
            
    def setAxisAcceleration(self, axis, acceleration):
        
        c_axis = ct.c_long(axis)
        c_acceleration = ct.c_long(acceleration)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        c_retVal = self.lib.SetOmsAxisAcceleration(self.handle, c_axis, c_acceleration)
        
        
        #ERROR HANDLING
        if(c_retVal == "SUCCESS"):
            self.addLog("Request was sent")
            
        elif(c_retVal == "COMMAND_TIME_OUT"):
            self.addLog("Command timed out")
            
        elif(c_retVal == "INVALID_AXIS_SELECTION"):
            self.addLog("Invalid axis value")
            
        elif(c_retVal == "INVALID PARAMETER"):
            self.addLog("Invalid acceleration parameter")
            
            
#--------------------------------------------------------------------------------------------------
            
    def getMotorAxisPosition(self, axis):
        
        #Determine which axis is being called
        if(axis == "1"):
            axisAsInt = 1
        
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
        
        
        ############################################################################################################
        # c_retval is an integer and comparing it to a string will always result in False
        # When it uses "SUCCESS" or "COMMAND_TIME_OUT" in the sample code it is not actually a string
        # those are defines that the compiler replaces with the integer value that they are defined as.
        # So you would want to compare c_retVal to an int value instead.
        # See the top of the file "OmsMAXkMC.h" to see what these are (under the section "/*  Function error code definitions  */")
        # I checked to see if we could access these defines through the dll, but there isn't a way.
        # I would recommend recreating those defines here (either with some global variables or a global dictionary).
        # But just using their literal values wouldn't be too bad of an option either, it would just make the code a little
        # harder to understand. Either way works.
        ############################################################################################################
        #ERROR HANDLING
        if(c_retVal == "SUCCESS"):
            self.addLog("Request was sent")
            
        elif(c_retVal == "COMMAND_TIME_OUT"):
            self.addLog("Command timed out")
            
        elif(c_retVal == "INVALID_AXIS_SELECTION"):
            self.addLog("Invalid axis value")
            
        position = ct.c_long(position).value
        
        return position
            
#--------------------------------------------------------------------------------------------------
            
    def moveOmsAxisRelativeWait(self, axis, position):
        
        #Setting time limit so that it will wait 5 seconds before signaling time out, is measured in milliseconds
        timeLim = 5000
        c_timeLim = ct.c_long(timeLim)
        
        c_axis = ct.c_long(axis)
        #position variable is sent over as a string but needs to be an int to convert to long
        position = int(position)
        c_position = ct.c_long(position)
        
        retVal = 0
        c_retVal = ct.c_long(retVal)
        
        c_retVal = self.lib.MoveOmsAxisRelWait(self.handle, c_axis, c_position, c_timeLim)
        
        
        #ERROR HANDLING
        if(c_retVal == "SUCCESS"):
            self.addLog("Request was sent")
            
        elif(c_retVal == "COMMAND_TIME_OUT"):
            self.addLog("Command timed out")
            
        elif(c_retVal == "INVALID_AXIS_SELECTION"):
            self.addLog("Invalid axis value")
            
        elif(c_retVal == "INVALID_PARAMETER"):
            self.addLog("Invalid position value")
            
        elif(c_retVal == "MOVE_TIME_OUT"):
            self.addLog("Timeout occurred before the move completed")
            
            
#--------------------------------------------------------------------------------------------------
            
    
        
        
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
