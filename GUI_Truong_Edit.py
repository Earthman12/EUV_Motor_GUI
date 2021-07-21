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

        #Status Message
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
        self.title.grid(row = 0, column = 1, padx = self.pad, pady = self.pad)
 
        #Controller Model
        self.modelLabel = tk.Label(text = "Controller Model: " + str(self.OmsLib.model.value))
        self.modelLabel.grid(row = 1, column = 1, padx = self.pad, pady = self.pad)

        #Command Label and Entry
        self.commandLabel = tk.Label(text = "Enter Command for the Controller:")
        self.commandLabel.grid(row = 2, column = 1)
        self.command = tk.Entry(width = 20)
        self.command.grid(row = 3, column = 1, padx = self.pad, pady = self.pad)

        #Send Command Button. After button is clicked, it sends command to Oms object and updates log
        #Command must be retrieved from Entry using .get() and needs to be converted to proper variable, haven't figured this out yet
        self.commandSend = self.command.get()
        self.commandSend = str(self.commandSend)
        self.commandButton = tk.Button(text = "Send", command = lambda :[self.OmsLib.sendCommand(self.commandSend), self.updateLog()])
        self.commandButton.grid(row = 4, column = 1, padx = self.pad, pady = self.pad)

        #Reset Button. Updates the log regarding if reset was successful or not
        self.resetButton = tk.Button(text = "Reset Controller", command = lambda : [self.OmsLib.resetController(), self.updateLog()])
        self.resetButton.grid(row = 1, column = 0, padx = self.pad, pady = self.pad)

        #Controller Log. Prints what controller is doing
        self.logLabel = tk.Label(text = "Controller Log: " + self.guiLog)
        self.logLabel.grid(row = 1, column = 2, padx = self.pad, pady = self.pad)
        
        self.updateLog()

       

#--------------------------------------------------------------------------------------------------

    #GUI function to update the log on the screen
    def updateLog(self):

        self.logLabel.config(text = "Controller Log: " + self.OmsLib.getLog())
   

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
        #pt DECLARES ITSELF AS C_CHAR_P VARIABLE 
        # * ALLOWS FOR VARIABLE NUMBER OF ARGUMENTS TO BE PASSED
        #map() LOOPS THROUGH FUNCTION ct.addressof WITH h BEING ONLY INTERABLE.
        #ct.addressof() RETURNS ADDRESS OF h AS AN INT
        h = [ct.create_string_buffer(b"OmsMAXk1")]
        pt = (ct.c_char_p)(*map(ct.addressof, h))

        self.handle = self.lib.GetOmsHandle(pt)
        print("handle: ", self.handle)
        
        #CONTROLLER LOG
        self.log = ""

        #OMS CONTROLLER MODEL
        self.model = self.getModel()

        #TRUE OR FALSE VALUE DETERMINING IF DRIVERS WERE LOADED
        self.libConnection = self.checkLibrary()

        #NEED THE MOTOR STILL

       

#--------------------------------------------------------------------------------------------------

       
    #FUNCTION THAT SHOULD RETURN THE MODEL OF THE CONTROLLER
    def getModel(self):

    	## Fix me
        #model = ct.c_wchar_p("")

        self.addLog("Attempting to retrieve model...")

        # model = ct.create_string_buffer(80)
        # print("model: ", model.value)
        
        # self.dver = self.lib.GetOmsDriverVersion(self.handle, model)
        # print("dver: ",self.dver)
        
        # print("model: ", model.value)

        # h = ct.create_string_buffer(b"wy")
        
        #CREATES MODEL COMMAND AND CONVERTS TO C
        cmd = "wy"
        cmd_ptr = ct.c_wchar_p(cmd)
        #MODEL VARIABLE DECLARED AS A C STRING BUFFER
        model = ct.create_string_buffer(80)
        print("model: ", model.value)
        retVal = self.lib.GetOmsControllerDescription( self.handle, model)
        if (retVal != 0): 
        	print("Big Not Success: " + str(retVal))
        print("model: ", model.value)

        if(model.value == "N/A"):

            self.addLog("Could not get model name.")

        elif(model.value == b""):

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

        # axmr1000;goid <--- COMMAND TO MOVE X AXIS 1000 STEPS

        returnStatus = 0
        c_returnStatus = ct.c_long(returnStatus)
        c_arg = ct.c_char_p(arg)
        
        c_returnStatus = self.lib.SendString(self.handle, c_arg)

        if(c_returnStatus == 1):
            self.addLog("Command timed out.")

        else:
            self.addLog("Command sent sucessfully")


#--------------------------------------------------------------------------------------------------


    def sendGetString(self, arg):

        response = ""

        returnStatus = self.lib.SendAndGetString(self.handle, arg, response)

        if(returnStatus == 1):
            self.addLog("Command timed out.")
            response = "N/A"

        elif(returnStatus == 2):
            self.addLog("Controller did not respond to command within 100 ms, signaled response time out.")
            response = "N/A"

        return str(response)


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