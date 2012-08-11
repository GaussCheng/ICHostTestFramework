'''
Created on Aug 9, 2012

@author: gausscheng
'''
import serial

class ICSerialTransceiver(object):
    '''
    classdocs
    '''


    def __init__(self, serial_dev):
        '''
        Constructor
        '''
        self.ser = serial.Serial(serial_dev, 115200, timeout = 0.05)
        print (self.ser)
    
    def read(self, size):
        '''
        Read
        '''
        return self.ser.read(size)   
    
    def write(self, data):
        '''
        Write
        '''
        self.ser.write(data)
    