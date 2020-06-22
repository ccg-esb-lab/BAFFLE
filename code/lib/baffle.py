

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
import dash_daq as daq
import json
import random
import pandas as pd
from ctypes import *
import sys
from time import sleep
import os, random, shutil, datetime, time
import serial as serial

import numpy as np
import matplotlib.pyplot as plt
import os, random, shutil, datetime, time
from time import sleep
from ctypes import *

#Phidget specific imports (stepper22)
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.Stepper import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *

from Phidget22.Devices.DigitalInput import DigitalInput

# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

import argparse

from pythonosc import udp_client

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=2345,
      help="The port the OSC server is listening on")
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)


################################### User-defined parameters
VERBOSE=True;

cameraOutput=1  #param
hubPort=0   #TMP

with_z_stepper=True
with_f_stepper=True
with_interface=True

timelapse_elapsed=0


fstepper_rescaleFactor=1 
zstepper_rescaleFactor=1 


fstepper_velocity=200
zstepper_velocity=200

fstepper_accelleration=1000
zstepper_accelleration=1000


output_channels=[ 'output_filterDARK', 'output_filterGFP', 'output_filterRFP','output_filterCFP','output_filterYFP','output_camera', 
        'output_incubator', 'output_defrost']
input_channels=[ 'input_zLimitSwitch', 'input_fLimitSwitch']


########################## Initialize InterfaceKit

f_stepper=Stepper()
z_stepper=Stepper()

interfaceKit_output= [DigitalOutput() for i in range (0, len(output_channels))]
interfaceKit_input= [DigitalInput() for i in range (0,len(input_channels))]

z_stepper_serial='506023'
f_stepper_serial='541630'
interfaceKit_serial='313877'  #dev: '313877'

#DEFAULT VALUES
fpos_filterBRIGHT=-3050
fpos_filterDARK=-3050
fpos_filterGFP=-6350
fpos_filterRFP=-4850
fpos_filterCFP=-1550
fpos_filterYFP=40

########################## Initialize variables
df_params = pd.DataFrame({
    'zpos': [0,50-2],
    'zpos_min':[1, 1],
    'zpos_max':[2, 1000],
    'zpos_delta':[3, 2],
    'fpos': [4,0],
    'fpos_min':[5, -10000],
    'fpos_max':[6, 10000],
    'fpos_delta':[7, 2],
    'fpos_filterBRIGHT':[8, fpos_filterBRIGHT],
    'fpos_filterDARK':[9, fpos_filterDARK],
    'fpos_filterGFP':[10, fpos_filterGFP],
    'fpos_filterRFP':[11, fpos_filterRFP],
    'fpos_filterCFP':[12, fpos_filterCFP],
    'fpos_filterYFP':[13, fpos_filterYFP],  
    'output_camera':[14, 5],  
    'output_filterBRIGHT':[15, 0],
    'output_filterDARK':[16, -1],
    'output_filterGFP':[17, 1],
    'output_filterRFP':[18, 2],
    'output_filterCFP':[19, 3],
    'output_filterYFP':[20, 4],
    'output_incubator':[21, 6],
    'output_defrost':[22, 7],
    'input_zLimitSwitch':[23, 1],
    'input_fLimitSwitch':[24, 0],
    'state_zLimitSwitch':[25, 1],
    'state_fLimitSwitch':[26, 0],
    'fstepper_rescaleFactor':[27, fstepper_rescaleFactor],
    'zstepper_rescaleFactor':[28, zstepper_rescaleFactor],
    'fstepper_velocity':[29, fstepper_velocity],
    'zstepper_velocity':[30, zstepper_velocity],
    'fstepper_accelleration':[31, fstepper_accelleration],
    'zstepper_accelleration':[32, zstepper_accelleration],
    'output_portDARK':[33, 2345],
    'output_ipDARK':[34, '127.0.0.1'],
    'interfaceKit_serial':[35, interfaceKit_serial],
    'f_stepper_serial':[36, f_stepper_serial],
    'z_stepper_serial':[37, z_stepper_serial]
})

def getParams():
    return df_params

def printParams():
    print(df_params)
    

###################################
arduino=serial.Serial('/dev/cu.usbmodem14231',9600)
    
    
###################################
    
def onAttachHandler(self):
    
    ph = self
    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.stepper.com/docs/Using_Multiple_stepper for information
    
        serialNumber = ph.getDeviceSerialNumber()
        channelClass = ph.getChannelClassName()
        channel = ph.getChannel()
        
        deviceClass = ph.getDeviceClass()
        if (deviceClass != DeviceClass.PHIDCLASS_VINT):
            print("\t" + channelClass + "\t (Serial Number: " + str(serialNumber) +
                  ") -> Channel:  " + str(channel) + "")
        else:            
            hubPort = ph.getHubPort()
            print("\t" + channelClass + "\t (Serial Number: " + str(serialNumber) +
                  ") -> Hub Port: " + str(hubPort) + "\t-> Channel:  " + str(channel) + "")
        
    except PhidgetException as e:
        print("Error in Attach Event:",e)
        #traceback.print_exc()
        return

def onDetachHandler(self):

    ph = self

    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.stepper.com/docs/Using_Multiple_stepper for information
        
        print("Detach Event:")
        
        serialNumber = ph.getDeviceSerialNumber()
        channelClass = ph.getChannelClassName()
        channel = ph.getChannel()
        
        deviceClass = ph.getDeviceClass()
        if (deviceClass != DeviceClass.PHIDCLASS_VINT):
            print("-> Channel Class: " + channelClass + "\t-> Serial Number: " + str(serialNumber) +
                  "\t-> Channel:  " + str(channel))
        else:            
            hubPort = ph.getHubPort()
            print("-> Channel Class: " + channelClass + "\t-> Serial Number: " + str(serialNumber) +
                  "\t-> Hub Port: " + str(hubPort) + "\t-> Channel:  " + str(channel) + "")
        
    except PhidgetException as e:
        print("Error in Detach Event:")
        #traceback.print_exc()
        return

def onErrorHandler(self, errorCode, errorString):

    sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")")

def onStateChangeHandler(self, state):
    deviceSerialNumber = self.getDeviceSerialNumber()
    if(self.linkedOutput.getAttached()):
        if state==1:  #Limit swith
            print(self.linkedOutput)
        
            
            #self.linkedOutput.setTargetPosition(self.linkedOutput.getPosition()) #Stop
            #if self.linkedOutput.getPosition()!=0:
            print("Stop @ %s | %s"%(df_params.loc[1,'fpos'],self.linkedOutput.getPosition()))  #limit switch
                
            #sleep(1)
            
#            this_acceleration=10000 #tmp
             #this_velocity=200 #df_params.loc[1,'fstepper_velocity'] 
#            this_rescale=1 #df_params.loc[1,'fstepper_rescaleFactor'] #tmp
#
#            print('*** f_stepper position: %s'%self.linkedOutput.getPosition())
#            
#            print("    f_stepper control mode: %s"%self.linkedOutput.getControlMode())
#
#            self.linkedOutput.setVelocityLimit(this_velocity)
#            print('    f_stepper velocity: %s'%self.linkedOutput.getVelocity())
#
#            self.linkedOutput.setAcceleration(this_acceleration)
#            print('    f_stepper acceleration: %s'%self.linkedOutput.getAcceleration())
#
#            self.linkedOutput.setRescaleFactor(this_rescale)  
#            print('    f_stepper rescale factor: %s'%self.linkedOutput.getRescaleFactor())
            
            self.linkedOutput.setTargetPosition(self.linkedOutput.getPosition()) #Stop
            
            df_params.loc[1,'fpos']=self.linkedOutput.getPosition()
            sleep(1)
            df_params.loc[1,'fpos_min']=self.linkedOutput.getPosition()+df_params.loc[1,'fpos_delta']
            
            print("Home: %s"%df_params.loc[1,'fpos_min'])
            
            self.linkedOutput.setTargetPosition(df_params.loc[1,'fpos_min']) 
            
            
def PrintEventDescriptions():
    print("--------------------")

    
##########################


def init_interface(interfaceKit_serial, hubPort, isHubPortDevice):
    
    if with_interface:    
        
        try:
            
            
            
            
            print("Connecting Output Channels (%s): %s"%(interfaceKit_serial, output_channels))
            for ich, this_channel in enumerate(output_channels):
                print("... %s: %s"%(ich,this_channel))
                ch=DigitalOutput()
                ch.setDeviceSerialNumber(interfaceKit_serial)
                
                ch.setHubPort(hubPort)
                ch.setIsHubPortDevice(isHubPortDevice)
                ch.setChannel(df_params.loc[1,this_channel])  
                ch.setOnAttachHandler(onAttachHandler)
                ch.setOnDetachHandler(onDetachHandler)
                ch.setOnErrorHandler(onErrorHandler)

                ch.openWaitForAttachment(5000)
                
                interfaceKit_output[ich]=ch
                
            print("Connecting Input Channels %s: %s"%(interfaceKit_serial, input_channels))
            for ich, this_channel in enumerate(input_channels):
                
               
                ch=DigitalInput()
                
                if ich==1: # 'input_zLimitSwitch', 'input_fLimitSwitch']
                    ch.linkedOutput = f_stepper
                    ch.linkedOutput.setOnPositionChangeHandler(positionChangeHandler)
                else:
                    ch.linkedOutput = z_stepper
                    ch.linkedOutput.setOnPositionChangeHandler(positionChangeHandler)
                
                ch.setOnStateChangeHandler(onStateChangeHandler)
                ch.setDeviceSerialNumber(interfaceKit_serial)
                ch.setHubPort(hubPort)
                ch.setIsHubPortDevice(isHubPortDevice)
                ch.setChannel(df_params.loc[1,this_channel])  
                ch.setOnAttachHandler(onAttachHandler)
                ch.setOnDetachHandler(onDetachHandler)
                ch.setOnErrorHandler(onErrorHandler)
                                 
                ch.openWaitForAttachment(5000)
                
                interfaceKit_input[ich]=ch
                
                
        except PhidgetException as e:
            print("Attachment Terminated: Open Failed", e)
            #traceback.print_exc()
            print("Cleaning up...")
            for ch in interfaceKit_output:
                ch.close()
            return False
        except RuntimeError as e:
             print("Attachment Terminated: RunTimeError", e)
             sys.stderr.write("Runtime Error: \t")
             #traceback.print_exc()
             return False

        
    return [interfaceKit_output, interfaceKit_input]


###########################################

def init_f_stepper(f_stepper, stepper_serial):
    if with_f_stepper:
        try:
            f_stepper.setOnAttachHandler(StepperAttached)
            f_stepper.setOnDetachHandler(StepperDetached)
            f_stepper.setOnErrorHandler(ErrorEvent)
            f_stepper.setDeviceSerialNumber(stepper_serial) 
            f_stepper.setOnPositionChangeHandler(positionChangeHandler)
            
            f_stepper.openWaitForAttachment(5000)
            f_stepper.setEngaged(1)
            #f_stepper.setCurrentLimit(1.5)
            #f_stepper.setAcceleration(10000)  #param
            
        except RuntimeError as e:
            print("Runtime Exception %s" % e.details)
            print("Press Enter to Exit...")
            readin = sys.stdin.read(1)
            exit(1)
    else:
        print('\t f_stepper not attached')

    return f_stepper



def init_z_stepper(z_stepper, stepper_serial):
    if with_z_stepper and z_stepper is not None:
        try:
            z_stepper.setOnAttachHandler(StepperAttached)
            z_stepper.setOnDetachHandler(StepperDetached)
            z_stepper.setOnErrorHandler(ErrorEvent)
            z_stepper.setOnPositionChangeHandler(positionChangeHandler)
            z_stepper.setDeviceSerialNumber(stepper_serial) 
            
            z_stepper.openWaitForAttachment(5000)
            z_stepper.setEngaged(1)
            #z_stepper.setAcceleration(10000) #param
        
        except RuntimeError as e:
            print("Runtime Exception %s" % e.details)
            print("Press Enter to Exit...")
            readin = sys.stdin.read(1)
            exit(1)
    else:
        print('\t z_stepper not attached')

    return z_stepper

########################################### Stepper functions
def StepperAttached(e):
    try:
        attached = e
        print("Attach Event Detected (Information Below)")
        print("===========================================")
        print("Library Version: %s" % attached.getLibraryVersion())
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("Channel Name: %s" % attached.getChannelName())
        print("Device ID: %d" % attached.getDeviceID())
        print("Device Version: %d" % attached.getDeviceVersion())
        print("Device Name: %s" % attached.getDeviceName())
        print("Device Class: %d" % attached.getDeviceClass())
        print("")

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...")
        readin = sys.stdin.read(1)
        exit(1)   
    
def StepperDetached(e):
    detached = e
    try:
        print("Detach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...")
        readin = sys.stdin.read(1)
        exit(1)   

def ErrorEvent(e, eCode, description):
    print("Error %i : %s" % (eCode, description))

def positionChangeHandler(e, position):
    print("Position: %s" % position)
    df_params.loc[1,'fpos']=position  #-df_params.loc[1,'fpos_min']
    #print("Serial: %f" % e.getSerialNumber())
    
def onStopChangeHandler(e, position):
    print("Stop! %s" % position)
    df_params.loc[1,'fpos']=position
    #print("Serial: %f" % e.getSerialNumber())
        

####################################### Z_STEPPER Functions
    

def Z_STEPPER_engage(z_stepper_serial):
    z_stepper_engaged=False
    #z_stepper=Stepper()
    
    if with_z_stepper:
        if z_stepper_serial is not None:
            init_z_stepper(z_stepper, z_stepper_serial)

        if z_stepper is not False:
            z_stepper_engaged=True
            print("> z_stepper engaged")
        else:
            print("> z_stepper NOT engaged")
    else:
        print("> z_stepper disabled")
        
    return z_stepper_engaged

def Z_STEPPER_disengage():
    z_stepper.close()
    print("> Z_STEPPER disengaged")
    return False    
    
def Z_STEPPER_isMoving():
    return z_stepper.getIsMoving()    
    
def Z_STEPPER_moveTo(zpos_target): 
    
    if z_stepper is not None:
        
        try:
            #z_stepper.setVelocityLimit(df_params['zstepper_velocity'][1])
            #print('z_stepper velocity: %s'%z_stepper.getVelocity())

            #z_stepper.setRescaleFactor(df_params['zstepper_rescaleFactor'][1])  
            #this_rescale=z_stepper.getRescaleFactor()
            #print('z_stepper rescale factor: %s'%this_rescale)

            #this_acceleration=z_stepper.getAcceleration()
            #print('z_stepper acceleration: %s'%this_rescale)
            
            
            #z_stepper.setCurrentLimit(2)
            print('moveTo: ',zpos_target)
            z_stepper.setTargetPosition(zpos_target)
        
        except RuntimeError as e:
            print('z-stepper not attached')
        
#        
#    
#def Z_STEPPER_setHome(): 
#    
#    if z_stepper is not None:
#        
#        try:
#            z_stepper.setRescaleFactor(df_params.loc[1,'zstepper_rescaleFactor'])  
#            this_rescale=z_stepper.getRescaleFactor()
#            print('z_stepper rescale factor: %s'%this_rescale)
#
#            this_acceleration=z_stepper.getAcceleration()
#            print('z_stepper acceleration: %s'%this_acceleration)
#
#            #Move continuously (until switch)
#            z_stepper.setControlMode(1)
#            print("z_stepper control mode: %s"%f_stepper.getControlMode())
#            z_stepper.setVelocityLimit(df_params.loc[1,'zstepper_velocity'])
#            
#        except RuntimeError as e:
#            print('z-stepper not attached')
        


##################################### F_STEPPER Functions
	

def F_STEPPER_engage(f_stepper_serial):
    #f_stepper=False
    #f_stepper=Stepper()
    
    f_stepper_engaged=False
    if with_f_stepper:
        if f_stepper_serial is not None:
            init_f_stepper(f_stepper, f_stepper_serial)

        if f_stepper is not False:
            f_stepper_engaged=True
            print("> f_stepper engaged")
        else:
            print("> f_stepper NOT engaged")
    else:
        print("> f_stepper disabled")
    
    return f_stepper_engaged

def F_STEPPER_disengage():
    f_stepper.close()
    #f_stepper=None
    print("> F_STEPPER_disengage")
    return False

def F_STEPPER_isMoving():
    return f_stepper.getIsMoving()
	
def F_STEPPER_moveTo(fpos_target):
    
    
    if with_f_stepper:
        
        #f_stepper.setVelocityLimit(df_params.loc[1,'fstepper_velocity'])
        #print('f_stepper velocity: %s'%f_stepper.getVelocity())
        
        #f_stepper.setRescaleFactor(df_params.loc[1,'fstepper_rescaleFactor'])  
        #this_rescale=f_stepper.getRescaleFactor()
        #print('f_stepper rescale factor: %s'%this_rescale)
        
        #this_acceleration=f_stepper.getAcceleration()
        
        f_stepper.setTargetPosition(fpos_target)
        
        print("> F_STEPPER_moveTo  (min: %s \t target: %s)"%(df_params.loc[1,'fpos_min'], fpos_target))
    
def F_STEPPER_setHome():
    if with_f_stepper:
        print("> F_STEPPER_setHome")
        
        this_acceleration=df_params.loc[1,'fstepper_velocity'] 
        this_velocity=df_params.loc[1,'fstepper_velocity'] 
        this_rescale=df_params.loc[1,'fstepper_rescaleFactor'] 
        
        #print("    f_stepper control mode: %s"%f_stepper.getControlMode())
            
        
        #f_stepper.setOnPositionChangeHandler(positionChangeHandler)
        f_stepper.setControlMode(1) #Move continuously (until switch)
        
        
        print('    f_stepper position: %s'%f_stepper.getPosition())

        f_stepper.setVelocityLimit(this_velocity)
        print('    f_stepper velocity: %s'%f_stepper.getVelocity())
        
        f_stepper.setAcceleration(this_acceleration)
        print('    f_stepper acceleration: %s'%f_stepper.getAcceleration())

        f_stepper.setRescaleFactor(this_rescale)  
        print('    f_stepper rescale factor: %s'%f_stepper.getRescaleFactor())
        
        #
        
        print("Moving...")
    
##################################### INTERFACEKIT Functions   

def INTERFACEKIT_engage(interfaceKit_serial):
    interface_engaged=False
    isHubPortDevice=False
    #channel=1 #tmp
    
    if with_interface:
        #interfaceKit_output=False
        if interfaceKit_serial is not None:
            init_interface(interfaceKit_serial, hubPort, isHubPortDevice)


        if interfaceKit_input is not False:  # or interfaceKit_input is not False  
            interface_engaged=True

        print("> INTERFACEKIT_engaged: %s"% interface_engaged)
    return interface_engaged


def INTERFACEKIT_disengage():
    if interfaceKit_output is not None:
        for ch in interfaceKit_output:
            ch.close()
        
    if interfaceKit_input is not None:
        for ch in interfaceKit_input:
            ch.close()
        interface_engaged=False
        print("> INTERFACEKIT_engaged: %s"%interface_engaged)
    return False


##################################### LED FUNCTIONS    
    
def LED_turnOFF(interfaceKit_output, channelID, LEDcolor, LEDoutput):

    if channelID=='DARK':
        
        #Here we communicate with rgb
        for i in range(1,9):
            cmd_enable='/Program/segment%s/enabled/'%i

            client.send_message(cmd_enable, [0])
            #print(cmd_enable,'0')
        
        print("> DARK_turnOFF (%s)"%(LEDcolor))
    else:
        interfaceKit_output[LEDoutput].setState(False)
        print("> CUBE_turnOFF (%s): channel %s"%(channelID, LEDoutput))
    
    return False
	
def LED_turnON(interfaceKit_output, channelID, LEDcolor, LEDoutput):
    
    if channelID=='DARK':
        #Here we communicate with protopixel
        #print('\nUpdating color of segments: %s'%thisLEDsegment)
        for i in range(1,9):
            cmd_enable='/Program/segment%s/enabled/'%i
            client.send_message(cmd_enable, [1])
    
    
        print("> DARK_turnON (%s)"%(LEDcolor))
    else:
        interfaceKit_output[LEDoutput].setState(True)
        print("> CUBE_turnON (%s): channel %s"%(channelID, LEDoutput))
        
    return True

##################################### INCUBATOR FUNCTIONS

def HEAT_turnON(interfaceKit_output, output_temperature):
    if with_interface:
        #print("> HEAT_turnON (%s) "%(output_temperature))

        interfaceKit_output[output_temperature].setState(True)
        
    return True

def HEAT_turnOFF(interfaceKit_output, output_temperature):
    if with_interface:
        #print("> HEAT_turnOFF (%s) "%(output_temperature))
        interfaceKit_output[output_temperature].setState(False)

    return False



##################################### CAMERA FUNCTIONS

def shoot_single(opt_config):
    
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    if VERBOSE:
        print('\t________ %s ________'%opt_config['channelID'])
        print('\t%s'%ts)
        print(opt_config)
    
    #MOVE FILTER POSITION
    
    if with_f_stepper:
        F_STEPPER_moveTo(opt_config['filterPos'])  
    
        maxLoops=20 #10 seconds
        nloops=0
        while F_STEPPER_isMoving() and nloops<maxLoops:
            sleep(0.5)
            print(".",nloops)  # ERROR: F_STEPPER_isMoving returns always 1
            
            nloops+=1
            
    #sleep(0.5)
    
    #TURN ON LED
    LED_turnON(interfaceKit_output, opt_config['channelID'], opt_config['ledColor'], opt_config['ledOutput'])
    time.sleep(0.5) 
    
    #TRIGGER CAMERA
    cameraOutput=df_params.loc[1,'output_camera']
    CAMERA_trigger(interfaceKit_output, cameraOutput, opt_config['exposure'])
    time.sleep(0.5) 
    
    #TURN OFF LED
    LED_turnOFF(interfaceKit_output, opt_config['channelID'], opt_config['ledColor'],opt_config['ledOutput'])
    time.sleep(0.5) 
    
    if VERBOSE:
        print(' ')
    else:
        print('%s\t%s\t%s sec'%(ts, opt_config['channelID'], opt_config['exposure']));

def shoot_multilight(opt_configs):
    print("> shoot_multilight:")
    
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    if VERBOSE:
        print('\t________________')
        print('\t%s'%ts)
        #print(opt_config)
    
    #MOVE FILTER POSITION (second in list)
    opt_config_pos0=opt_configs[1]
    if with_f_stepper:
        F_STEPPER_moveTo(opt_config_pos0['filterPos'])  
    
        maxLoops=20 #10 seconds
        nloops=0
        while F_STEPPER_isMoving() and nloops<maxLoops:
            sleep(0.5)
            print(".",nloops)  # ERROR: F_STEPPER_isMoving returns always 1
            
            nloops+=1
    else:
        print('Not moving to ',opt_config_pos0['filterPos'])    
    #sleep(0.5)
    
    #Turn on lights
    for this_opt_config in opt_configs:
        #TURN ON LED
        LED_turnON(interfaceKit_output, this_opt_config['channelID'], this_opt_config['ledColor'], this_opt_config['ledOutput'])
        time.sleep(0.5) 

    #TRIGGER CAMERA
    cameraOutput=df_params.loc[1,'output_camera']
    CAMERA_trigger(interfaceKit_output, cameraOutput, opt_config_pos0['exposure'])  #Also of second in list
    time.sleep(0.5) 

    #Turn off lights    
    for this_opt_config in opt_configs:
        #TURN OFF LED
        LED_turnOFF(interfaceKit_output, this_opt_config['channelID'], this_opt_config['ledColor'], this_opt_config['ledOutput'])
        time.sleep(0.5) 
    
    #if VERBOSE:
    #    print(' ')
    #else:
    #    print('%s\t%s\t%s sec'%(ts, opt_config['channelID'], opt_config['exposure']));
    
        
def shoot_multichannel(opt_configs):  
    print("> shoot_multichannel:")
    for this_opt_config in opt_configs:
        shoot_single(this_opt_config)
        
def CAMERA_trigger(interfaceKit_output, cameraOutput, texposure):
    
    interfaceKit_output[cameraOutput].setState(True);
    time.sleep(texposure) 
    interfaceKit_output[cameraOutput].setState(False);
    
    if VERBOSE:
        print('\tClick! (ch: %s, exp:%s sec)'%(cameraOutput, texposure));
        

##################################### AUXILIARY FUNCTIONS


def toString(opt_configs):
    for this_opt_config in opt_configs:
        print(this_opt_config)
