'''
Created on Aug 11, 2012

@author: gausscheng
'''
from ic_communicate.ic_serial_transceiver import ICSerialTransceiver

class ICTesterInterface(object):
    '''
    test case interface
    '''

    g_serial_transceiver = ICSerialTransceiver("/dev/ttyS0")

    def __init__(self):
        '''
        Constructor
        '''
        
    def load(self, str_content):
        return False
    
    def case_name(self):
        return ""
    
    def run_case(self):
        return self.case_name() + "test fail!"
    
    def err_code(self):
        return 0
    
    def err_descr(self):
        return ""
    
    def test_report(self):
        return ""