

import pandas as pd
import sys
from time import sleep
import time, datetime
import serial as serial

#Phidget specific imports (stepper22)
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.Stepper import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *

from Phidget22.Devices.DigitalInput import DigitalInput

################################### User-defined parameters
VERBOSE=False;

cameraOutput=1  
hubPort=0   

with_z_stepper=True
with_f_stepper=True
with_interface=True
with_arduino=True

timelapse_elapsed=0

fstepper_rescaleFactor=1 
zstepper_rescaleFactor=1 

fstepper_velocity=2000
zstepper_velocity=2000

fstepper_accelleration=1000 
zstepper_accelleration=1000

output_channels=[ 'output_filterDARK', 'output_filterGFP', 'output_filterRFP','output_filterCFP','output_filterYFP','output_camera', 
        'output_incubator', 'output_humidity']
input_channels=[ 'input_zLimitSwitch', 'input_fLimitSwitch']

########################## Initialize InterfaceKit

f_stepper=Stepper()
z_stepper=Stepper()

interfaceKit_output= [DigitalOutput() for i in range (0, len(output_channels))]
interfaceKit_input= [DigitalInput() for i in range (0,len(input_channels))]


########################## USER-DEFINED PARAMETERS

#MODIFY TO DEFINE SERIAL NUMBERS!!
z_stepper_serial='506023'
f_stepper_serial='522559' 
interfaceKit_serial='313877' 
arduino_usbport='/dev/ttyUSB0' 

#DEFAULT VALUES
fpos_filterBRIGHT=-3250
fpos_filterDARK=-3250
fpos_filterGFP=-4994
fpos_filterRFP=-6555
fpos_filterCFP=-1690
fpos_filterYFP=-160

zpos_min=1
zpos_max=45000

fpos_min=-7000
fpos_max=1

if(with_arduino):
    arduino=serial.Serial(arduino_usbport,115200)  

########################## Initialize variables
df_params = pd.DataFrame({
    'zpos': [0,1],
    'zpos_min':[1, zpos_min],
    'zpos_max':[2, zpos_max],
    'zpos_delta':[3, 2],
    'fpos': [4,1],
    'fpos_min':[5, fpos_min],
    'fpos_max':[6, fpos_max],
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
    'output_humidity':[22, 7],
    'input_zLimitSwitch':[23, 0],
    'input_fLimitSwitch':[24, 1],
    'state_zLimitSwitch':[25, 0],
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
    'z_stepper_serial':[37, z_stepper_serial],
    'arduino_usbport':[38, arduino_usbport]
})

def getParams():
    return df_params

def printParams():
    print(df_params)
    
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

def fonStateChangeHandler(self, state):
    deviceSerialNumber = self.getDeviceSerialNumber()
    if(self.linkedOutput.getAttached()):
        if state==1:  #Limit swith
        
            if VERBOSE: 
                print("Stop (F) @ %s | %s"%(df_params.loc[1,'fpos'],self.linkedOutput.getPosition()))  #limit switch
               
            self.linkedOutput.setTargetPosition(self.linkedOutput.getPosition()) #Stop
            
            df_params.loc[1,'fpos']=self.linkedOutput.getPosition()
            sleep(1)
            
            df_params.loc[1,'fpos_max']=self.linkedOutput.getPosition()
            df_params.loc[1,'fpos_min']=self.linkedOutput.getPosition()+fpos_min
            
            df_params.loc[1,'fpos_filterBRIGHT']=df_params.loc[1,'fpos_max']+fpos_filterBRIGHT
            #print("Bright: %s "%(df_params.loc[1,'fpos_filterBRIGHT']))
                  
            df_params.loc[1,'fpos_filterDARK']=df_params.loc[1,'fpos_max']+fpos_filterDARK
            #print("Dark: %s "%(df_params.loc[1,'fpos_filterDARK']))
                  
            df_params.loc[1,'fpos_filterGFP']=df_params.loc[1,'fpos_max']+fpos_filterGFP
            #print("GFP: %s "%(df_params.loc[1,'fpos_filterGFP']))
                  
            df_params.loc[1,'fpos_filterRFP']=df_params.loc[1,'fpos_max']+fpos_filterRFP
            #print("RFP: %s "%(df_params.loc[1,'fpos_filterRFP']))
                  
            df_params.loc[1,'fpos_filterCFP']=df_params.loc[1,'fpos_max']+fpos_filterCFP
            #print("CFP: %s "%(df_params.loc[1,'fpos_filterCFP']))
                  
            df_params.loc[1,'fpos_filterYFP']=df_params.loc[1,'fpos_max']+fpos_filterYFP
            #print("YFP: %s "%(df_params.loc[1,'fpos_filterYFP']))
            
            print("Home (F): %s [%s,%s]"%(df_params.loc[1,'fpos'],df_params.loc[1,'fpos_min'],df_params.loc[1,'fpos_max']))
            
            self.linkedOutput.setVelocityLimit(fstepper_velocity)
            next_fpos=df_params.loc[1,'fpos_filterBRIGHT']
            self.linkedOutput.setTargetPosition(next_fpos)
            

def zonStateChangeHandler(self, state):
    deviceSerialNumber = self.getDeviceSerialNumber()
    if(self.linkedOutput.getAttached()):
        if state==1:  #Limit swith
        
            if VERBOSE: 
                print("Stop (Z) @ %s | %s"%(df_params.loc[1,'zpos'],self.linkedOutput.getPosition()))  #limit switch
               
            self.linkedOutput.setTargetPosition(self.linkedOutput.getPosition()) #Stop
            
            df_params.loc[1,'zpos']=self.linkedOutput.getPosition()
            sleep(0.5)
            
            df_params.loc[1,'zpos_max']=self.linkedOutput.getPosition()+zpos_max
            df_params.loc[1,'zpos_min']=self.linkedOutput.getPosition()
            
            print("Home (Z): %s [%s,%s]"%(df_params.loc[1,'zpos'],df_params.loc[1,'zpos_min'],df_params.loc[1,'zpos_max']))
            
            self.linkedOutput.setVelocityLimit(zstepper_velocity)
            
            next_zpos=df_params.loc[1,'zpos_min']+5000.0
            self.linkedOutput.setTargetPosition(next_zpos)
            
            
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
                
                interfaceKit_output[ich].setState(False)  #init off
                
            print("Connecting Input Channels %s: %s"%(interfaceKit_serial, input_channels))
            for ich, this_channel in enumerate(input_channels):
                
               
                ch=DigitalInput()
                
                if ich==1: # 'input_zLimitSwitch', 'input_fLimitSwitch']
                    ch.linkedOutput = f_stepper
                    ch.linkedOutput.setOnPositionChangeHandler(fpositionChangeHandler)
                    ch.setOnStateChangeHandler(fonStateChangeHandler)
                else:
                    ch.linkedOutput = z_stepper
                    ch.linkedOutput.setOnPositionChangeHandler(zpositionChangeHandler)
                    ch.setOnStateChangeHandler(zonStateChangeHandler)
                    
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
            print("Cleaning up...")
            for ch in interfaceKit_output:
                ch.close()
            return False
        except RuntimeError as e:
            print("Attachment Terminated: RunTimeError", e)
            sys.stderr.write("Runtime Error: \t")
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
            f_stepper.setOnPositionChangeHandler(fpositionChangeHandler)
            
            f_stepper.openWaitForAttachment(5000)
            f_stepper.setEngaged(1)
            f_stepper.setCurrentLimit(1.5)
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
            z_stepper.setOnPositionChangeHandler(zpositionChangeHandler)
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

def fpositionChangeHandler(e, position):
    #print("fpositionChangeHandler: %s" % position)
    df_params.loc[1,'fpos']=position  #-df_params.loc[1,'fpos_min']
    #print("Serial: %f" % e.getSerialNumber())
    
def fonStopChangeHandler(e, position):
    #print("fonStopChangeHandler: %s" % position)
    df_params.loc[1,'fpos']=position
    #print("Serial: %f" % e.getSerialNumber())
    
def zpositionChangeHandler(e, position):
    #print("zpositionChangeHandler: %s" % position)
    df_params.loc[1,'zpos']=position  #-df_params.loc[1,'fpos_min']
    #print("Serial: %f" % e.getSerialNumber())
    
def zonStopChangeHandler(e, position):
    #print("zonStopChangeHandler: %s" % position)
    df_params.loc[1,'zpos']=position
    #print("Serial: %f" % e.getSerialNumber())
        

####################################### Z_STEPPER Functions
    

def Z_STEPPER_engage(z_stepper_serial):
    z_stepper_engaged=False
    
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
            z_stepper.setVelocityLimit(df_params['zstepper_velocity'][1])
            if VERBOSE: 
                print('z_moveTo: ',zpos_target)
            z_stepper.setTargetPosition(zpos_target)
        
        except RuntimeError as e:
            print('z-stepper not attached')
        
#        
#    
def Z_STEPPER_setHome(): 
#    
    if z_stepper is not None:
#        
        try:
            this_velocity=2000 #df_params.loc[1,'zstepper_velocity'] 
            z_stepper.setVelocityLimit(this_velocity)
            z_stepper.setTargetPosition(-2*(df_params.loc[1,'zpos_max']))

            if VERBOSE: 
                print("(Z) Moving...")

        except RuntimeError as e:
            print('z-stepper not attached')
        


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
        
        if VERBOSE: 
            print('moveTo: ',fpos_target)
        f_stepper.setTargetPosition(fpos_target)
        
        #print("> F_STEPPER_moveTo  (min: %s \t target: %s)"%(df_params.loc[1,'fpos_min'], fpos_target))
    
def F_STEPPER_setHome():
    if with_f_stepper:
        if VERBOSE: 
            print("> F_STEPPER_setHome")
        
        
        this_velocity=500 #df_params.loc[1,'fstepper_velocity'] 
        
        f_stepper.setVelocityLimit(this_velocity)
        f_stepper.setTargetPosition(2*abs(df_params.loc[1,'fpos_min']))
       
        
        if VERBOSE: 
            print("(F) Moving...")
    
    
##################################### ARDUINO Functions   

def ARDUINO_engage(arduino_usbport):
    arduino_engaged=False
  
    if with_arduino:
        
        arduino_engaged=True

        print("> ARDUINO_engaged: %s"% arduino_engaged)
    return arduino_engaged


def ARDUINO_disengage():
    if with_arduino:
        
        #HERE WE DISENGAGE ARDUINO
        #arduino.close()   
        
        arduino_engaged=False
        print("> ARDUINO_engaged: %s"%arduino_engaged)
    return False

##################################### INTERFACEKIT Functions   

def INTERFACEKIT_engage(interfaceKit_serial):
    interface_engaged=False
    isHubPortDevice=False
    
    if with_interface:
        if interfaceKit_serial is not None:
            init_interface(interfaceKit_serial, hubPort, isHubPortDevice)


        if interfaceKit_input is not False:  
            interface_engaged=True
            print(output_channels[0])
            
            LED_turnOFF(interfaceKit_output, "BRIGHT", "", df_params.loc[1,'output_filterBRIGHT'])
        

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
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def LED_turnOFF(interfaceKit_output, channelID, LEDcolor, LEDoutput):

    if channelID=='DARK':
        
        #Here we communicate with rgb  !!!!!!!!!!!!
        serialStr="<0,0,0,0,0>"
        if VERBOSE: 
            print("Sending to serial: ",serialStr)
        
        #Here we send data to arduino via serial
        arduino.write(serialStr.encode())
        
        #for i in range(1,9):
            #cmd_enable='/Program/segment%s/enabled/'%i

            #client.send_message(cmd_enable, [0])
            #print(cmd_enable,'0')
            
        if VERBOSE: 
            print("> DARK_turnOFF")
        
    elif channelID=='BRIGHT':
        interfaceKit_output[LEDoutput].setState(True)
        if VERBOSE: 
            print("> BRIGHT_turnOFF: channel %s"%(LEDoutput))
    else:
        interfaceKit_output[LEDoutput].setState(False)
        if VERBOSE: 
            print("> CUBE_turnOFF (%s): channel %s"%(channelID, LEDoutput))
    
    return False
	
def LED_turnON(interfaceKit_output, channelID, LEDcolor, LEDoutput):
    
    if channelID=='DARK':
        
        serialStr=""
        if "#" in LEDcolor:  #Format: #FFFFF
            
            strLEDcolor=LEDcolor.split(',')
            
            rgbcolor=hex_to_rgb(strLEDcolor[0])
            #rgbalpha=strLEDcolor[1]
            rgbalpha="1"  #Temp 
            
            serialStr="<%s,%s,%s,%s,%s>"%(str(0), rgbcolor[0], rgbcolor[1], rgbcolor[2], rgbalpha)
        else:
            serialStr="<%s,%s,%s,%s,%s>"%(str(0), str(LEDcolor['rgb']['r']),str(LEDcolor['rgb']['g']),str(LEDcolor['rgb']['b']), str(LEDcolor['rgb']['a']))
        if VERBOSE: 
            print("Sending to serial: ",serialStr.encode())
        
        arduino.write(serialStr.encode())
        
    
        if VERBOSE: 
            print("> DARK_turnON (%s)"%(LEDcolor))
        
    
    elif channelID=='BRIGHT':
        interfaceKit_output[LEDoutput].setState(False)
        
        if VERBOSE:
            print("> BRIGHT_turnON: channel %s"%(LEDoutput))
    else:
        interfaceKit_output[LEDoutput].setState(True)
        
        if VERBOSE:
            print("> CUBE_turnON (%s): channel %s"%(channelID, LEDoutput))
        
    return True

##################################### INCUBATOR FUNCTIONS

def HEAT_turnON(interfaceKit_output, output_temperature):
    if with_arduino:
        if with_interface:
            try:
                #print("> HEAT_turnON (pin:%s) "%(output_temperature))

                interfaceKit_output[output_temperature].setState(True)
            
            except PhidgetException as e:
                print("Error in Attach Event:",e)
        
    return True

def HEAT_turnOFF(interfaceKit_output, output_temperature):
    if with_arduino:
        if with_interface:
            try:
                #print("> HEAT_turnOFF (pin:%s) "%(output_temperature))
                interfaceKit_output[output_temperature].setState(False)

            except PhidgetException as e:
                print("Error in Attach Event:",e)

    return False


def HUMIDITY_turnON(interfaceKit_output, output_humidity):
    if with_arduino:
        if with_interface:
            try:
                #print("> HUMIDITY_turnON (pin:%s) "%(output_humidity))

                interfaceKit_output[output_humidity].setState(True)
            
            except PhidgetException as e:
                print("Error in Attach Event:",e)
        
    return True

def HUMIDITY_turnOFF(interfaceKit_output, output_humidity):
    if with_arduino:
        if with_interface:
            try:
                #print("> HUMIDITY_turnOFF (pin:%s) "%(output_humidity))
                interfaceKit_output[output_humidity].setState(False)
            
            except PhidgetException as e:
                print("Error in Attach Event:",e)

    return False



##################################### CAMERA FUNCTIONS

def shoot_single(opt_config, this_temperature, this_humidity):
    
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
            
            nloops+=1
            
    #sleep(0.5)
    
    min_exposure=0.5
    if opt_config['exposure']>min_exposure:

        #TURN ON LED
        LED_turnON(interfaceKit_output, opt_config['channelID'], opt_config['ledColor'], opt_config['ledOutput'])
        time.sleep(0.5) 

        #TRIGGER CAMERA
        cameraOutput=df_params.loc[1,'output_camera']
        CAMERA_trigger(interfaceKit_output, cameraOutput, opt_config['exposure'])
        time.sleep(opt_config['exposure']+1) 

        #TURN OFF LED
        LED_turnOFF(interfaceKit_output, opt_config['channelID'], opt_config['ledColor'],opt_config['ledOutput'])
        time.sleep(0.5) 

        
    else:
        
        if VERBOSE:
            print("Exposure time too short for Bulb >> Strobo")
        
        #TRIGGER CAMERA
        time.sleep(5) 
        
        cameraOutput=df_params.loc[1,'output_camera']
        interfaceKit_output[cameraOutput].setState(True);
    
        #CAMERA_trigger(interfaceKit_output, cameraOutput, opt_config['exposure']+1)
        time.sleep(1) 
        
         #TURN ON LED
        LED_turnON(interfaceKit_output, opt_config['channelID'], opt_config['ledColor'], opt_config['ledOutput'])
        time.sleep(opt_config['exposure']) 
        
        #TURN OFF LED
        LED_turnOFF(interfaceKit_output, opt_config['channelID'], opt_config['ledColor'],opt_config['ledOutput'])
        time.sleep(1) 
        
        #UNTRIGGER CAMERA
        interfaceKit_output[cameraOutput].setState(False);
        
        

    print('%s\t%s\t%s\t%s\t%s sec'%(ts, this_temperature, this_humidity, opt_config['channelID'], opt_config['exposure']));
    time.sleep(1) 

def shoot_multilight(opt_configs, this_temperature, this_humidity):
    
    if VERBOSE:
        print("> light:")
    
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
            #print(".",nloops)  # ERROR: F_STEPPER_isMoving returns always 1
            
            nloops+=1
    #else:
        #print('Not moving to ',opt_config_pos0['filterPos'])    
    #sleep(0.5)
    
    if VERBOSE:
        print(">>>> Exposure:",opt_config_pos0['exposure'])
    
    min_exposure=0.5
    if opt_config_pos0['exposure']>min_exposure:

        #Turn on lights
        for this_opt_config in opt_configs:
            #TURN ON LED
            LED_turnON(interfaceKit_output, this_opt_config['channelID'], this_opt_config['ledColor'], this_opt_config['ledOutput'])
            time.sleep(1 )

        #TRIGGER CAMERA
        cameraOutput=df_params.loc[1,'output_camera']
        CAMERA_trigger(interfaceKit_output, cameraOutput, opt_config_pos0['exposure'])  #Also of second in list
        time.sleep(1) 

        #Turn off lights    
        for this_opt_config in opt_configs:
            #TURN OFF LED
            LED_turnOFF(interfaceKit_output, this_opt_config['channelID'], this_opt_config['ledColor'], this_opt_config['ledOutput'])
            time.sleep(1) 
    #else:
        
        #print("Exposure time too short for Bulb")
        
    time.sleep(1) 
    
    
    print('%s\t%s\t%s\t%s\t%s sec'%(ts, this_temperature, this_humidity, opt_config['channelID'], opt_config['exposure']));
    #if VERBOSE:
    #    print(' ')
    #else:
    #    print('%s\t%s\t%s sec'%(ts, opt_config['channelID'], opt_config['exposure']));
    
        
def shoot_multichannel(opt_configs, this_temperature, this_humidity):  
    #print("> shoot_multichannel:")
    for this_opt_config in opt_configs:
        shoot_single(this_opt_config, this_temperature, this_humidity)
        time.sleep(1) 
        
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
