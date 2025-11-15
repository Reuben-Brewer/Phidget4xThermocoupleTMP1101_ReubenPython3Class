# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision B, 11/14/2025

Verified working on: Python 3.11/3.12 for Windows 10, 11 64-bit.
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################

##########################################
from LowPassFilterForDictsOfLists_ReubenPython2and3Class import *
##########################################

##########################################
import os
import sys
import platform
import time
import datetime
import math
import queue as Queue
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
import subprocess
import numpy
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
import signal #for CTRLc_HandlerFunction
##########################################

##########################################
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.TemperatureSensor import *
##########################################

##########################################
try:
    import platform

    if platform.system() == "Windows":
        import ctypes
        winmm = ctypes.WinDLL('winmm')
        winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.

except:
    print("Phidget4xThermocoupleTMP1101_ReubenPython3Class,winmm.timeBeginPeriod(1) failed.")
##########################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
class Phidget4xThermocoupleTMP1101_ReubenPython3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, SetupDict): #Subclass the Tkinter Frame

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        print("#################### Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.MainThread_StillRunningFlag = 0
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        self.NumberOfTemperatureSensorChannels = 4

        self.TemperatureSensorList_PhidgetsTemperatureSensorObjects = list()

        self.TemperatureSensorList_AttachedAndOpenFlag = [0.0] * self.NumberOfTemperatureSensorChannels
        self.TemperatureSensorList_UpdateDeltaTseconds = [0.0] * self.NumberOfTemperatureSensorChannels
        self.TemperatureSensorList_UpdateFrequencyHz = [0.0] * self.NumberOfTemperatureSensorChannels
        self.TemperatureSensorList_ErrorCallbackFiredFlag = [0.0] * self.NumberOfTemperatureSensorChannels

        self.TemperatureSensorList_Value_DegC_Raw = [-11111.0] * self.NumberOfTemperatureSensorChannels
        self.TemperatureSensorList_Value_DegC_Filtered = [-11111.0] * self.NumberOfTemperatureSensorChannels

        self.TemperatureSensorList_Value_DegC_LowPassFilter_ReubenPython2and3ClassObject = list()
        
        self.TemperatureSensorList_ListOfOnAttachCallbackFunctionNames = [self.TemperatureSensor0onAttachCallback, self.TemperatureSensor1onAttachCallback, self.TemperatureSensor2onAttachCallback, self.TemperatureSensor3onAttachCallback]
        self.TemperatureSensorList_ListOfOnDetachCallbackFunctionNames = [self.TemperatureSensor0onDetachCallback, self.TemperatureSensor1onDetachCallback, self.TemperatureSensor2onDetachCallback, self.TemperatureSensor3onDetachCallback]
        self.TemperatureSensorList_ListOfOnErrorCallbackFunctionNames = [self.TemperatureSensor0onErrorCallback, self.TemperatureSensor1onErrorCallback, self.TemperatureSensor2onErrorCallback, self.TemperatureSensor3onErrorCallback]

        self.MostRecentDataDict = dict()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.CurrentTime_CalculatedFromGUIthread = -11111.0
        self.LastTime_CalculatedFromGUIthread = -11111.0
        self.StartingTime_CalculatedFromGUIthread = -11111.0
        self.DataStreamingFrequency_CalculatedFromGUIthread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromGUIthread = -11111.0
        self.LoopCounter_CalculatedFromDedicatedGUIthread = 0

        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0
        self.LoopCounter_CalculatedFromMainThread = 0
        #########################################################
        #########################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if "GUIparametersDict" in SetupDict:

            GUIparametersDict = SetupDict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "root" in GUIparametersDict:
                self.root = GUIparametersDict["root"]
            else:
                print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: ERROR, must pass in 'root'")
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            ##########################################
            if "GUI_ROWSPAN" in GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in GUIparametersDict:
                self.GUI_STICKY = str(GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: GUIparametersDict: " + str(GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UsePhidgetsLoggingInternalToThisClassObjectFlag" in SetupDict:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UsePhidgetsLoggingInternalToThisClassObjectFlag", SetupDict["UsePhidgetsLoggingInternalToThisClassObjectFlag"])
        else:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = 1

        print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: UsePhidgetsLoggingInternalToThisClassObjectFlag: " + str(self.UsePhidgetsLoggingInternalToThisClassObjectFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "LogFileNameFullPath" in SetupDict:
            self.LogFileNameFullPath = str(SetupDict["LogFileNameFullPath"])

            if os.path.isdir("self.LogFileNameFullPath") == 0:
                print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__:  Error, 'LogFileNameFullPath' must be FULL path (should include slashes).")
                self.LogFileNameFullPath = os.path.join(os.getcwd(), "Phidget4xThermocoupleTMP1101_ReubenPython3Class_PhidgetLog.txt")

        else:
            self.LogFileNameFullPath = os.path.join(os.getcwd(), "Phidget4xThermocoupleTMP1101_ReubenPython3Class_PhidgetLog.txt")

        print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: LogFileNameFullPath: " + str(self.LogFileNameFullPath))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "WaitForAttached_TimeoutDuration_Milliseconds" in SetupDict:
            self.WaitForAttached_TimeoutDuration_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WaitForAttached_TimeoutDuration_Milliseconds", SetupDict["WaitForAttached_TimeoutDuration_Milliseconds"], 0.0, 60000.0))

        else:
            self.WaitForAttached_TimeoutDuration_Milliseconds = 5000

        print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: WaitForAttached_TimeoutDuration_Milliseconds: " + str(self.WaitForAttached_TimeoutDuration_Milliseconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VINT_DesiredSerialNumber" in SetupDict:
            try:
                self.VINT_DesiredSerialNumber = int(SetupDict["VINT_DesiredSerialNumber"])
            except:
                print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: Error, VINT_DesiredSerialNumber invalid.")
        else:
            self.VINT_DesiredSerialNumber = -1

        print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: VINT_DesiredSerialNumber: " + str(self.VINT_DesiredSerialNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VINT_DesiredPortNumber" in SetupDict:

            try:
                self.VINT_DesiredPortNumber = int(SetupDict["VINT_DesiredPortNumber"])
            except:
                print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: Error, VINT_DesiredPortNumber invalid.")

        else:
            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: Error, must initialize object with 'VINT_DesiredPortNumber' argument.")
            return

        print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: VINT_DesiredPortNumber: " + str(self.VINT_DesiredPortNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredDeviceID" in SetupDict:

            try:
                self.DesiredDeviceID = int(SetupDict["DesiredDeviceID"])
            except:
                print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: Error, DesiredDeviceID invalid.")

        else:
            self.DesiredDeviceID = -1

        print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: DesiredDeviceID: " + str(self.DesiredDeviceID))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in SetupDict:
            self.NameToDisplay_UserSet = str(SetupDict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in SetupDict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", SetupDict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.010

        print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        if "TemperatureSensorList_Value_DegCExponentialSmoothingFilterLambda" in SetupDict:
            self.TemperatureSensorList_Value_DegCExponentialSmoothingFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("TemperatureSensorList_Value_DegCExponentialSmoothingFilterLambda", SetupDict["TemperatureSensorList_Value_DegCExponentialSmoothingFilterLambda"], 0.0, 1.0)

        else:
            self.TemperatureSensorList_Value_DegCExponentialSmoothingFilterLambda = 0.95 #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: TemperatureSensorList_Value_DegCExponentialSmoothingFilterLambda: " + str(self.TemperatureSensorList_Value_DegCExponentialSmoothingFilterLambda))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.TemperatureSensorList_ChannelsToIgnore = []

        if "TemperatureSensorList_ChannelsToIgnore" in SetupDict:
            TemperatureSensorList_ChannelsToIgnore_TEMP = SetupDict["TemperatureSensorList_ChannelsToIgnore"]

            if isinstance(TemperatureSensorList_ChannelsToIgnore_TEMP, list) == 1:
                for Element in TemperatureSensorList_ChannelsToIgnore_TEMP:
                    if Element in range(0, self.NumberOfTemperatureSensorChannels):
                        self.TemperatureSensorList_ChannelsToIgnore.append(Element)

        print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: TemperatureSensorList_ChannelsToIgnore: " + str(self.TemperatureSensorList_ChannelsToIgnore))
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings = dict([("DataStreamingFrequency_CalculatedFromMainThread", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                                                            ("DataStreamingFrequency_CalculatedFromGUIthread", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1), ("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                                                            ("TemperatureSensorList_Value_DegC", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1), ("ExponentialSmoothingFilterLambda", self.TemperatureSensorList_Value_DegCExponentialSmoothingFilterLambda)]))])

        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_SetupDict = dict([("DictOfVariableFilterSettings", self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings)])

        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject = LowPassFilterForDictsOfLists_ReubenPython2and3Class(self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_SetupDict)
        self.LOWPASSFILTER_OPEN_FLAG = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG
        #########################################################

        #########################################################
        if self.LOWPASSFILTER_OPEN_FLAG != 1:
            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: Failed to open LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.")
            return
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ######################################################### MUST OPEN THE DEVICE BEFORE WE CAN QUERY ITS INFORMATION
        #########################################################
        try:
            TemperatureSensor_OpenedTemporarilyJustToGetDeviceInfo = TemperatureSensor()

            if self.VINT_DesiredSerialNumber != -1:
                TemperatureSensor_OpenedTemporarilyJustToGetDeviceInfo.setDeviceSerialNumber(self.VINT_DesiredSerialNumber)

            TemperatureSensor_OpenedTemporarilyJustToGetDeviceInfo.setChannel(0)
            TemperatureSensor_OpenedTemporarilyJustToGetDeviceInfo.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)

            self.DetectedDeviceName = TemperatureSensor_OpenedTemporarilyJustToGetDeviceInfo.getDeviceName()
            print("Phidget4xThermocoupleTMP1101_ReubenPython2and3Class __init__: DetectedDeviceName: " + self.DetectedDeviceName)

            self.VINT_DetectedSerialNumber = TemperatureSensor_OpenedTemporarilyJustToGetDeviceInfo.getDeviceSerialNumber()
            print("Phidget4xThermocoupleTMP1101_ReubenPython2and3Class __init__: VINT_DetectedSerialNumber: " + str(self.VINT_DetectedSerialNumber))

            self.DetectedDeviceID = TemperatureSensor_OpenedTemporarilyJustToGetDeviceInfo.getDeviceID()
            print("Phidget4xThermocoupleTMP1101_ReubenPython2and3Class __init__: DetectedDeviceID: " + str(self.DetectedDeviceID))

            self.DetectedDeviceVersion = TemperatureSensor_OpenedTemporarilyJustToGetDeviceInfo.getDeviceVersion()
            print("Phidget4xThermocoupleTMP1101_ReubenPython2and3Class __init__: DetectedDeviceVersion: " + str(self.DetectedDeviceVersion))

            self.DetectedDeviceLibraryVersion = TemperatureSensor_OpenedTemporarilyJustToGetDeviceInfo.getLibraryVersion()
            print("Phidget4xThermocoupleTMP1101_ReubenPython2and3Class __init__: DetectedDeviceLibraryVersion: " + str(self.DetectedDeviceLibraryVersion))

            TemperatureSensor_OpenedTemporarilyJustToGetDeviceInfo.close()

        except PhidgetException as e:
            print("Phidget4xThermocoupleTMP1101_ReubenPython2and3Class __init__: Failed to call Device Information, Phidget Exception %i: %s" % (e.code, e.details))
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.VINT_DesiredSerialNumber != -1: #'-1' means we should open the device regardless os serial number.
            if self.VINT_DetectedSerialNumber != self.VINT_DesiredSerialNumber:
                print("Phidget4xThermocoupleTMP1101_ReubenPython2and3Class __init__: The desired Serial Number (" + str(self.VINT_DesiredSerialNumber) + ") does not match the detected serial number (" + str(self.VINT_DetectedSerialNumber) + ").")
                return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.DesiredDeviceID != -1:
            if self.DetectedDeviceID != self.DesiredDeviceID:
                print("The DesiredDeviceID (" + str(self.DesiredDeviceID) + ") does not match the detected Device ID (" + str(self.DetectedDeviceID) + ").")
                self.CloseDevice()
                return
        #########################################################
        #########################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.PhidgetsDeviceConnectedFlag = 0
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            if self.UsePhidgetsLoggingInternalToThisClassObjectFlag == 1:
                try:
                    Log.enable(LogLevel.PHIDGET_LOG_INFO, self.LogFileNameFullPath)
                    print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: Enabled Phidget Logging.")
                except PhidgetException as e:
                    print("Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__: Failed to enable Phidget Logging, Phidget Exception %i: %s" % (e.code, e.details))
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            for TemperatureSensorChannel in range(0, self.NumberOfTemperatureSensorChannels):

                self.TemperatureSensorList_PhidgetsTemperatureSensorObjects.append(TemperatureSensor())

                ##########################################################################################################
                ##########################################################################################################
                if TemperatureSensorChannel not in self.TemperatureSensorList_ChannelsToIgnore:

                    print("Creating TemperatureSensorChannel: " + str(TemperatureSensorChannel))

                    ##########################################################################################################
                    try:
                        if self.VINT_DesiredSerialNumber != -1:
                            self.TemperatureSensorList_PhidgetsTemperatureSensorObjects[TemperatureSensorChannel].setDeviceSerialNumber(self.VINT_DesiredSerialNumber)

                    except PhidgetException as e:
                        print("Phidget4xThermocoupleTMP1101_ReubenPython2and3Class __init__: setDeviceSerialNumber, Phidget Exception %i: %s" % (e.code, e.details))
                    ##########################################################################################################

                    ##########################################################################################################
                    try:
                        self.TemperatureSensorList_PhidgetsTemperatureSensorObjects[TemperatureSensorChannel].setChannel(TemperatureSensorChannel)

                    except PhidgetException as e:
                        print("Phidget4xThermocoupleTMP1101_ReubenPython2and3Class __init__: setChannel, Phidget Exception %i: %s" % (e.code, e.details))
                    ##########################################################################################################

                    ##########################################################################################################
                    try:
                        self.TemperatureSensorList_PhidgetsTemperatureSensorObjects[TemperatureSensorChannel].setOnAttachHandler(self.TemperatureSensorList_ListOfOnAttachCallbackFunctionNames[TemperatureSensorChannel])

                    except PhidgetException as e:
                        print("Phidget4xThermocoupleTMP1101_ReubenPython2and3Class __init__: setOnAttachHandler, Phidget Exception %i: %s" % (e.code, e.details))
                    ##########################################################################################################

                    ##########################################################################################################
                    try:
                        self.TemperatureSensorList_PhidgetsTemperatureSensorObjects[TemperatureSensorChannel].setOnDetachHandler(self.TemperatureSensorList_ListOfOnDetachCallbackFunctionNames[TemperatureSensorChannel])

                    except PhidgetException as e:
                        print("Phidget4xThermocoupleTMP1101_ReubenPython2and3Class __init__: setOnDetachHandler, Phidget Exception %i: %s" % (e.code, e.details))
                    ##########################################################################################################

                    ##########################################################################################################
                    try:
                        self.TemperatureSensorList_PhidgetsTemperatureSensorObjects[TemperatureSensorChannel].setOnErrorHandler(self.TemperatureSensorList_ListOfOnErrorCallbackFunctionNames[TemperatureSensorChannel])

                    except PhidgetException as e:
                        print("Phidget4xThermocoupleTMP1101_ReubenPython2and3Class __init__: setOnErrorHandler, Phidget Exception %i: %s" % (e.code, e.details))
                    ##########################################################################################################

                    ##########################################################################################################
                    try:
                        self.TemperatureSensorList_PhidgetsTemperatureSensorObjects[TemperatureSensorChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)

                    except PhidgetException as e:
                        print("Phidget4xThermocoupleTMP1101_ReubenPython2and3Class __init__: openWaitForAttachment, Phidget Exception %i: %s" % (e.code, e.details))
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.PhidgetsDeviceConnectedFlag = 1
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except PhidgetException as e:
            self.PhidgetsDeviceConnectedFlag = 0
            print("Phidget4xThermocoupleTMP1101_ReubenPython2and3Class __init__: Failed to attach, Phidget Exception %i: %s" % (e.code, e.details))
            traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if self.PhidgetsDeviceConnectedFlag == 1:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
            self.MainThread_ThreadingObject.start()
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            if self.USE_GUI_FLAG == 1:
                self.StartGUI(self.root)
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.CTRLc_RegisterHandlerFunction()
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        print("#################### Phidget4xThermocoupleTMP1101_ReubenPython3Class __init__ ending. ####################")
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensorGENERALonAttachCallback(self, TemperatureSensorChannel):

        try:

            ##########################################################################################################
            self.TemperatureSensorList_PhidgetsTemperatureSensorObjects[TemperatureSensorChannel].setDataRate(50)
            self.TemperatureSensorList_PhidgetsTemperatureSensorObjects[TemperatureSensorChannel].setTemperatureChangeTrigger(0)

            self.MyPrint_WithoutLogFile("TemperatureSensorGENERALonAttachCallback event, TemperatureSensorChannel " +
                                        str(TemperatureSensorChannel) +
                                        ", DataRateHz: " +
                                        str(self.TemperatureSensorList_PhidgetsTemperatureSensorObjects[TemperatureSensorChannel].getDataInterval()) +
                                        ", TemperatureChangeTrigger: " +
                                        str(self.TemperatureSensorList_PhidgetsTemperatureSensorObjects[TemperatureSensorChannel].getTemperatureChangeTrigger()))
            ##########################################################################################################

            self.TemperatureSensorList_AttachedAndOpenFlag[TemperatureSensorChannel] = 1

            self.MyPrint_WithoutLogFile("$$$$$$$$$$ TemperatureSensorGENERALonAttachCallback event for TemperatureSensorChannel " +
                                        str(TemperatureSensorChannel) +
                                        ", Attached! $$$$$$$$$$")

        except PhidgetException as e:
            self.TemperatureSensorList_AttachedAndOpenFlag[TemperatureSensorChannel] = 0
            self.MyPrint_WithoutLogFile("TemperatureSensorGENERALonAttachCallback event for TemperatureSensorChannel " + str(TemperatureSensorChannel) + ", ERROR: Failed to attach, Phidget Exception %i: %s" % (e.code, e.details))
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensorGENERALonDetachCallback(self, TemperatureSensorChannel):

        self.TemperatureSensorList_AttachedAndOpenFlag[TemperatureSensorChannel] = 0

        self.MyPrint_WithoutLogFile("$$$$$$$$$$ TemperatureSensorGENERALonDetachCallback event for TemperatureSensorChannel " +
                                    str(TemperatureSensorChannel) +
                                    ", Detatched! $$$$$$$$$$")

        try:
            self.TemperatureSensorList_PhidgetsTemperatureSensorObjects[TemperatureSensorChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            time.sleep(0.250)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("TemperatureSensorGENERALonDetachCallback event for Channel " + str(TemperatureSensorChannel) + ", failed to openWaitForAttachment, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensorGENERALonErrorCallback(self, TemperatureSensorChannel, code, description):

        if TemperatureSensorChannel not in self.TemperatureSensorList_ChannelsToIgnore:
            self.TemperatureSensorList_ErrorCallbackFiredFlag[TemperatureSensorChannel] = 1
            self.MyPrint_WithoutLogFile("TemperatureSensorGENERALonErrorCallback event for Channel " + str(TemperatureSensorChannel) + ", Error Code " + ErrorEventCode.getName(code) + ", description: " + str(description))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor0onAttachCallback(self, HandlerSelf):

        TemperatureSensorChannel = 0
        self.TemperatureSensorGENERALonAttachCallback(TemperatureSensorChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor0onDetachCallback(self, HandlerSelf):

        TemperatureSensorChannel = 0
        self.TemperatureSensorGENERALonDetachCallback(TemperatureSensorChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor0onVoltageRatioChangeCallback(self, HandlerSelf, VoltageRatio):

        TemperatureSensorChannel = 0
        self.TemperatureSensorGENERALonVoltageRatioChangeCallback(TemperatureSensorChannel, VoltageRatio)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor0onErrorCallback(self, HandlerSelf, code, description):

        TemperatureSensorChannel = 0
        self.TemperatureSensorGENERALonErrorCallback(TemperatureSensorChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################





    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor1onAttachCallback(self, HandlerSelf):

        TemperatureSensorChannel = 1
        self.TemperatureSensorGENERALonAttachCallback(TemperatureSensorChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor1onDetachCallback(self, HandlerSelf):

        TemperatureSensorChannel = 1
        self.TemperatureSensorGENERALonDetachCallback(TemperatureSensorChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor1onVoltageRatioChangeCallback(self, HandlerSelf, VoltageRatio):

        TemperatureSensorChannel = 1
        self.TemperatureSensorGENERALonVoltageRatioChangeCallback(TemperatureSensorChannel, VoltageRatio)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor1onErrorCallback(self, HandlerSelf, code, description):

        TemperatureSensorChannel = 1
        self.TemperatureSensorGENERALonErrorCallback(TemperatureSensorChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################





    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor2onAttachCallback(self, HandlerSelf):

        TemperatureSensorChannel = 2
        self.TemperatureSensorGENERALonAttachCallback(TemperatureSensorChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor2onDetachCallback(self, HandlerSelf):

        TemperatureSensorChannel = 2
        self.TemperatureSensorGENERALonDetachCallback(TemperatureSensorChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor2onVoltageRatioChangeCallback(self, HandlerSelf, VoltageRatio):

        TemperatureSensorChannel = 2
        self.TemperatureSensorGENERALonVoltageRatioChangeCallback(TemperatureSensorChannel, VoltageRatio)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor2onErrorCallback(self, HandlerSelf, code, description):

        TemperatureSensorChannel = 2
        self.TemperatureSensorGENERALonErrorCallback(TemperatureSensorChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################





    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor3onAttachCallback(self, HandlerSelf):

        TemperatureSensorChannel = 3
        self.TemperatureSensorGENERALonAttachCallback(TemperatureSensorChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor3onDetachCallback(self, HandlerSelf):

        TemperatureSensorChannel = 3
        self.TemperatureSensorGENERALonDetachCallback(TemperatureSensorChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor3onVoltageRatioChangeCallback(self, HandlerSelf, VoltageRatio):

        TemperatureSensorChannel = 3
        self.TemperatureSensorGENERALonVoltageRatioChangeCallback(TemperatureSensorChannel, VoltageRatio)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureSensor3onErrorCallback(self, HandlerSelf, code, description):

        TemperatureSensorChannel = 3
        self.TemperatureSensorGENERALonErrorCallback(TemperatureSensorChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################





    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CTRLc_RegisterHandlerFunction(self):

        CurrentHandlerRegisteredForSIGINT = signal.getsignal(signal.SIGINT)
        defaultish = (signal.SIG_DFL, signal.SIG_IGN, None, getattr(signal, "default_int_handler", None)) #Treat Python's built-in default handler as "unregistered"

        if CurrentHandlerRegisteredForSIGINT in defaultish:  # Only install if it's default/ignored (i.e., nobody set it yet)
            signal.signal(signal.SIGINT, self.CTRLc_HandlerFunction)
            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class, CTRLc_RegisterHandlerFunction event fired!")

        else:
            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class, could not register CTRLc_RegisterHandlerFunction (already registered previously)")
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## MUST ISSUE CTRLc_RegisterHandlerFunction() AT START OF PROGRAM
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CTRLc_HandlerFunction(self, signum, frame):

        print("Phidget4xThermocoupleTMP1101_ReubenPython3Class, CTRLc_HandlerFunction event firing!")

        self.ExitProgram_Callback()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_FloatOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = float(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber, ExitProgramIfFailureFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a numerical value, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1.0:
                return InputNumber_ConvertedToFloat

            else:

                print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. '" +
                              str(InputNameString) +
                              "' must be 0 or 1 (value was " +
                              str(InputNumber_ConvertedToFloat) +
                              "). Press any key (and enter) to exit.")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()

                else:
                    return -1
                ##########################

            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue, ExitProgramIfFailureFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        try:
            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a float value, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat_Limited = self.LimitNumber_FloatOutputOnly(RangeMinValue, RangeMaxValue, InputNumber_ConvertedToFloat)

            if InputNumber_ConvertedToFloat_Limited != InputNumber_ConvertedToFloat:
                print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be in the range [" +
                      str(RangeMinValue) +
                      ", " +
                      str(RangeMaxValue) +
                      "] (value was " +
                      str(InputNumber_ConvertedToFloat) + ")")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()
                else:
                    return -11111.0
                ##########################

            else:
                return InputNumber_ConvertedToFloat_Limited
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict()  # So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread_Filtered(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                DataStreamingFrequency_CalculatedFromMainThread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromMainThread", DataStreamingFrequency_CalculatedFromMainThread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromMainThread = ResultsDict["DataStreamingFrequency_CalculatedFromMainThread"]["Filtered_MostRecentValuesList"][0]

            self.LoopCounter_CalculatedFromMainThread = self.LoopCounter_CalculatedFromMainThread + 1
            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_GUIthread_Filtered(self):

        try:
            self.CurrentTime_CalculatedFromGUIthread = self.getPreciseSecondsTimeStampString()

            self.DataStreamingDeltaT_CalculatedFromGUIthread = self.CurrentTime_CalculatedFromGUIthread - self.LastTime_CalculatedFromGUIthread

            if self.DataStreamingDeltaT_CalculatedFromGUIthread != 0.0:
                DataStreamingFrequency_CalculatedFromGUIthread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromGUIthread

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromGUIthread", DataStreamingFrequency_CalculatedFromGUIthread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromGUIthread = ResultsDict["DataStreamingFrequency_CalculatedFromGUIthread"]["Filtered_MostRecentValuesList"][0]

            self.LoopCounter_CalculatedFromDedicatedGUIthread = self.LoopCounter_CalculatedFromDedicatedGUIthread + 1
            self.LastTime_CalculatedFromGUIthread = self.CurrentTime_CalculatedFromGUIthread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_GUIthread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertAngleToAllUnits(self, InputAngle, UnitsStr, VelocityFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:             

            ##########################################################################################################
            ##########################################################################################################
            if VelocityFlag == 0:

                ##########################################################################################################
                ConvertedValuesDict =  dict([("PhidgetsUnits", -11111.0),
                                            ("Deg", -11111.0),
                                            ("Rad", -11111.0),
                                            ("Rev", -11111.0)])

                if UnitsStr not in self.Position_ListOfAcceptableUnitString:
                    print("ConvertAngleToAllUnits: Error, Units must be in " + str(self.Position_ListOfAcceptableUnitString))
                    return ConvertedValuesDict
                ##########################################################################################################
                
            else:
                ##########################################################################################################
                ConvertedValuesDict =  dict([("PhidgetsUnitsPerSec", -11111.0),
                                            ("DegPerSec", -11111.0),
                                            ("RadPerSec", -11111.0),
                                            ("RevPerSec", -11111.0)])
                
                if UnitsStr not in self.Velocity_ListOfAcceptableUnitString:
                    print("ConvertAngleToAllUnits: Error, Units must be in " + str(self.Velocity_ListOfAcceptableUnitString))
                    return ConvertedValuesDict
                ##########################################################################################################

            InputAngle = float(InputAngle)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            if UnitsStr.find("PhidgetsUnits") != -1: #Could include velocity units wqith "PerSec" in it.
                ConvertedValue_PhidgetsUnits = InputAngle
                ConvertedValue_Deg = self.DegPerStep*(ConvertedValue_PhidgetsUnits/self.MicrostepsPerStep)
                ConvertedValue_Rev = ConvertedValue_Deg / 360.0
                ConvertedValue_Rad = ConvertedValue_Rev * 2.0 * math.pi
            ##########################################################################################################

            ##########################################################################################################
            elif UnitsStr.find("Deg") != -1: #Could include velocity units wqith "PerSec" in it.
                ConvertedValue_Deg = InputAngle
                ConvertedValue_PhidgetsUnits = self.MicrostepsPerStep*(ConvertedValue_Deg/self.DegPerStep)
                ConvertedValue_Rev = ConvertedValue_Deg / 360.0
                ConvertedValue_Rad = ConvertedValue_Rev * 2.0 * math.pi
            ##########################################################################################################

            ##########################################################################################################
            elif UnitsStr.find("Rad") != -1: #Could include velocity units wqith "PerSec" in it.
                ConvertedValue_Rad = InputAngle
                ConvertedValue_Deg = ConvertedValue_Rad*180.0/math.pi
                ConvertedValue_Rev = ConvertedValue_Deg/360.0
                ConvertedValue_PhidgetsUnits = self.MicrostepsPerStep*(ConvertedValue_Deg/self.DegPerStep)
            ##########################################################################################################

            ##########################################################################################################
            elif UnitsStr.find("Rev") != -1: #Could include velocity units wqith "PerSec" in it.
                ConvertedValue_Rev = InputAngle
                ConvertedValue_Rad = ConvertedValue_Rev*2.0*math.pi
                ConvertedValue_Deg = ConvertedValue_Rev*360.0
                ConvertedValue_PhidgetsUnits = self.MicrostepsPerStep*(ConvertedValue_Deg/self.DegPerStep)
            ##########################################################################################################

            ##########################################################################################################
            else:
                pass
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if VelocityFlag == 0:
                ConvertedValuesDict = dict([("PhidgetsUnits", ConvertedValue_PhidgetsUnits),
                                            ("Deg", ConvertedValue_Deg),
                                            ("Rad", ConvertedValue_Rad),
                                            ("Rev", ConvertedValue_Rev)])
            else:
                ConvertedValuesDict = dict([("PhidgetsUnitsPerSec", ConvertedValue_PhidgetsUnits),
                                            ("DegPerSec", ConvertedValue_Deg),
                                            ("RadPerSec", ConvertedValue_Rad),
                                            ("RevPerSec", ConvertedValue_Rev)])
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            return ConvertedValuesDict
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("ConvertPositionToAllUnits InputAngle: " + str(InputAngle) + ", exceptions: %s" % exceptions)
            #traceback.print_exc()
            return ConvertedValuesDict
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for Phidget4xThermocoupleTMP1101_ReubenPython3Class object.")
        self.MainThread_StillRunningFlag = 1

        ##########################################################################################################
        pass
        ##########################################################################################################

        ##########################################################################################################
        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            try:

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                Temperature_DegC_TemporaryValue = [-11111.11]*self.NumberOfTemperatureSensorChannels

                for TemperatureSensorChannel in range(0, self.NumberOfTemperatureSensorChannels):

                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    try:
                        if TemperatureSensorChannel not in self.TemperatureSensorList_ChannelsToIgnore: #Can't read temperature from a channel that's unhooked or has an error.
                            Temperature_DegC_TemporaryValue[TemperatureSensorChannel] = self.TemperatureSensorList_PhidgetsTemperatureSensorObjects[TemperatureSensorChannel].getTemperature()

                    except PhidgetException as ex:
                        print("self.TemperatureSensorList_PhidgetsTemperatureSensorObjects.getTemperature(TemperatureSensorChannel): PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)
                        Temperature_DegC_TemporaryValue[TemperatureSensorChannel] = -11111.111
                        traceback.print_exc()
                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################

                    #print("Temperature_DegC_TemporaryValue[TemperatureSensorChannel]: " + str(Temperature_DegC_TemporaryValue[TemperatureSensorChannel]))

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                AddDataDictFromExternalProgram_ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("TemperatureSensorList_Value_DegC", Temperature_DegC_TemporaryValue)])) #Update ENTIRE list in a SINGLE function call
                self.TemperatureSensorList_Value_DegC_Raw = AddDataDictFromExternalProgram_ResultsDict["TemperatureSensorList_Value_DegC"]["Raw_MostRecentValuesList"]
                self.TemperatureSensorList_Value_DegC_Filtered = AddDataDictFromExternalProgram_ResultsDict["TemperatureSensorList_Value_DegC"]["Filtered_MostRecentValuesList"]
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.MostRecentDataDict["Time"] = self.CurrentTime_CalculatedFromMainThread

                self.MostRecentDataDict["CurrentTime_CalculatedFromMainThread"] = self.CurrentTime_CalculatedFromMainThread
                self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromMainThread"] = self.DataStreamingFrequency_CalculatedFromMainThread

                self.MostRecentDataDict["TemperatureSensorList_Value_DegC_Raw"] = self.TemperatureSensorList_Value_DegC_Raw
                self.MostRecentDataDict["TemperatureSensorList_Value_DegC_Filtered"] = self.TemperatureSensorList_Value_DegC_Filtered
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.UpdateFrequencyCalculation_MainThread_Filtered()

                if self.MainThread_TimeToSleepEachLoop > 0.0:
                    if self.MainThread_TimeToSleepEachLoop > 0.001:
                        time.sleep(self.MainThread_TimeToSleepEachLoop - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                    else:
                        time.sleep(self.MainThread_TimeToSleepEachLoop)
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("MainThread, exceptions: %s" % exceptions)
                traceback.print_exc()

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:
            self.CloseDevice()

        except:
            pass

        self.MyPrint_WithoutLogFile("Finished MainThread for Phidget4xThermocoupleTMP1101_ReubenPython3Class object.")
        self.MainThread_StillRunningFlag = 0
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CloseDevice(self):

        try:

            ##########################################################################################################
            self.TemperatureSensor_Object.close()
            ##########################################################################################################

            ##########################################################################################################
            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class: CloseDevice, event fired!")
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("Phidget4xThermocoupleTMP1101_ReubenPython3Class: CloseDevice, Exceptions: %s" % exceptions)
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for Phidget4xThermocoupleTMP1101_ReubenPython3Class object")

        self.EXIT_PROGRAM_FLAG = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateVariableFilterSettingsFromExternalProgram(self, VariableNameString, UseMedianFilterFlag, UseExponentialSmoothingFilterFlag, ExponentialSmoothingFilterLambda, PrintInfoForDebuggingFlag=0):
        try:

            self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.UpdateVariableFilterSettingsFromExternalProgram(VariableNameString, UseMedianFilterFlag, UseExponentialSmoothingFilterFlag, ExponentialSmoothingFilterLambda)

            self.TemperatureSensorList_Value_DegCExponentialSmoothingFilterLambda = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.GetMostRecentDataDict()["TemperatureSensorList_Value_DegC"]["ExponentialSmoothingFilterLambda"]

            ##########################################################################################################
            if PrintInfoForDebuggingFlag==1:
                print("UpdateVariableFilterSettingsFromExternalProgram: "
                      "VariableNameString: " + str(VariableNameString) +
                      ", UseMedianFilterFlag " + str(UseMedianFilterFlag) +
                      ", UseExponentialSmoothingFilterFlag: " + str(UseExponentialSmoothingFilterFlag) +
                      ", ExponentialSmoothingFilterLambda: " + str(ExponentialSmoothingFilterLambda))

                print("UpdateVariableFilterSettingsFromExternalProgram: self.TemperatureSensorList_Value_DegCExponentialSmoothingFilterLambda: " + str(self.TemperatureSensorList_Value_DegCExponentialSmoothingFilterLambda))
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("UpdateVariableFilterSettingsFromExternalProgram, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent):

        self.GUI_Thread(GuiParent)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent):

        print("Starting the GUI_Thread for Phidget4xThermocoupleTMP1101_ReubenPython3Class object.")

        #################################################
        #################################################
        #################################################
        self.root = parent
        self.parent = parent
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.TkinterScaleLabelWidth = 30
        self.TkinterScaleWidth = 10
        self.TkinterScaleLength = 250
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=50)

        self.DeviceInfo_Label["text"] = self.NameToDisplay_UserSet + \
                                         "\nDevice Name: " + self.DetectedDeviceName + \
                                         "\nVINT SerialNumber: " + str(self.VINT_DetectedSerialNumber) + \
                                         "\nDeviceID: " + str(self.DetectedDeviceID) + \
                                         "\nFW Ver: " + str(self.DetectedDeviceVersion) + \
                                         "\nLibrary Ver: " + str(self.DetectedDeviceLibraryVersion)

        self.DeviceInfo_Label.grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.Data_Label = Label(self.myFrame, text="Data_Label", width=120)
        self.Data_Label.grid(row=1, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=10, rowspan=1)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=3, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=10, rowspan=10)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################
        #################################################
        #################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                #######################################################
                #######################################################
                try:

                    #######################################################
                    #######################################################
                    #######################################################
                    self.Data_Label["text"] = self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict)
                    #######################################################
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    #######################################################
                    self.UpdateFrequencyCalculation_GUIthread_Filtered()
                    #######################################################
                    #######################################################
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("Phidget4xThermocoupleTMP1101_ReubenPython3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

        number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

        ListOfStringsToJoin = []

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if isinstance(input, str) == 1:
            ListOfStringsToJoin.append(input)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
            element = float(input)
            prefix_string = "{:." + str(number_of_decimal_places) + "f}"
            element_as_string = prefix_string.format(element)

            ##########################################################################################################
            ##########################################################################################################
            if element >= 0:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
                element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
            else:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
            ##########################################################################################################
            ##########################################################################################################

            ListOfStringsToJoin.append(element_as_string)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, list) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, tuple) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, dict) == 1:

            if len(input) > 0:
                for Key in input: #RECURSION
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a dict()
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        else:
            ListOfStringsToJoin.append(str(input))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if len(ListOfStringsToJoin) > 1:

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            StringToReturn = ""
            for Index, StringToProcess in enumerate(ListOfStringsToJoin):

                ################################################
                if Index == 0: #The first element
                    if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                        StringToReturn = "{"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                        StringToReturn = "("
                    else:
                        StringToReturn = "["

                    StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
                ################################################

                ################################################
                elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                    StringToReturn = StringToReturn + StringToProcess + ", "
                ################################################

                ################################################
                else: #The last element
                    StringToReturn = StringToReturn + StringToProcess

                    if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                        StringToReturn = StringToReturn + "}"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                        StringToReturn = StringToReturn + ")"
                    else:
                        StringToReturn = StringToReturn + "]"

                ################################################

            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        elif len(ListOfStringsToJoin) == 1:
            StringToReturn = ListOfStringsToJoin[0]

        else:
            StringToReturn = ListOfStringsToJoin

        return StringToReturn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertDictToProperlyFormattedStringForPrinting(self, DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

        try:
            ProperlyFormattedStringForPrinting = ""
            ItemsPerLineCounter = 0

            for Key in DictToPrint:

                ##########################################################################################################
                if isinstance(DictToPrint[Key], dict): #RECURSION
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                         str(Key) + ":\n" + \
                                                         self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key],
                                                                                                              NumberOfDecimalsPlaceToUse,
                                                                                                              NumberOfEntriesPerLine,
                                                                                                              NumberOfTabsBetweenItems)

                else:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                         str(Key) + ": " + \
                                                         self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key],
                                                                                                                                               0,
                                                                                                                                               NumberOfDecimalsPlaceToUse)
                ##########################################################################################################

                ##########################################################################################################
                if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                    ItemsPerLineCounter = ItemsPerLineCounter + 1
                else:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                    ItemsPerLineCounter = 0
                ##########################################################################################################

            return ProperlyFormattedStringForPrinting

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertDictToProperlyFormattedStringForPrinting, Exceptions: %s" % exceptions)
            return ""
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################