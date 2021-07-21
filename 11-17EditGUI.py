import ctypes as ct
import tkinter as tk
import functools as ft


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
        

        currRow = 1
        currCol = 3
        for motorNum in range(1,8):
            motorNumStr = str(motorNum)
            # Frame
            motorFrame = tk.LabelFrame(self.root, text = "Motor #"+motorNumStr, relief = "ridge")
            motorFrame.grid(row = currRow, column = currCol)

            # Motor Position
            motorPos = tk.Label(motorFrame, text = ("Axis #"+motorNumStr+" motor position: " + str(self.OmsLib.getMotorAxisPosition(motorNumStr))))
            motorPos.grid(row = 0, column = 1)

            # Motor commands
            motorLabel = tk.Label(motorFrame, text = "Enter number of steps to move relative to its position:")
            motorLabel.grid(row = 1, column = 0)
            # Entry
            motorEntry = tk.Entry(motorFrame, width = 10)
            motorEntry.grid(row = 2, column = 0)
            # Send button
            motorButton = tk.Button(motorFrame, text = "Send", command = lambda n=motorNum, entry=motorEntry : [self.OmsLib.moveOmsAxisRelativeWait(n, int(entry.get())), self.updateLog()])
            motorButton.grid(row = 3, column = 0)

            # Base veloctiy controls
            baseVelocityLabel = tk.Label(motorFrame, text = "Set base velocity:")
            baseVelocityLabel.grid(row = 1, column = 1)
            # Entry
            baseVelocityEntry = tk.Entry(motorFrame, width = 10)
            baseVelocityEntry.grid(row = 2, column = 1)
            # Button
            baseVelocityButton = tk.Button(motorFrame, text = "Set", command = lambda n=motorNum, entry=baseVelocityEntry  : [self.OmsLib.setAxisBaseVelocity(n, int(entry.get())), self.updateLog()])
            baseVelocityButton.grid(row = 3, column = 1)

            # Velocity control options
            velocityLabel = tk.Label(motorFrame, text = "Set velocity:")
            velocityLabel.grid(row = 1, column = 2)
            # Entry
            velocityEntry = tk.Entry(motorFrame, width = 10)
            velocityEntry.grid(row = 2, column = 2)
            # Button
            velocityButton = tk.Button(motorFrame, text = "Set", command = lambda n=motorNum, entry=velocityEntry  : [self.OmsLib.setAxisVelocity(n, int(entry.get())), self.updateLog()])
            velocityButton.grid(row = 3, column = 2)

            # Acceleration control options
            accelerationLabel = tk.Label(motorFrame, text = "Set acceleration:")
            accelerationLabel.grid(row = 1, column = 3)
            # Entry
            accelerationEntry = tk.Entry(motorFrame, width = 10)
            accelerationEntry.grid(row = 2, column = 3)
            # Button
            accelerationButton = tk.Button(motorFrame, text = "Set", command = lambda n=motorNum, entry=accelerationEntry  : [self.OmsLib.setAxisAcceleration(n, int(entry.get())), self.updateLog()])
            accelerationButton.grid(row = 3, column = 3)

            # if (motorNum == 4):
            #     currRow = 1
            #     currCol += 1 
            # else:    
            #     currRow += 1

            currRow += 1
            
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
        
        c_axis = ct.c_long(self.axis)
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
        
        c_axis = ct.c_long(self.axis)
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
        
        print(self.axis)
        print(axisAsInt)
    
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
        
        self.axis = self.determineAxisAsInt(axis)
        self.position = position
        
        #Setting time limit so that it will wait 5 seconds before signaling time out, is measured in milliseconds
        timeLim = 5000
        c_timeLim = ct.c_long(timeLim)
        
        c_axis = ct.c_long(self.axis)
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
