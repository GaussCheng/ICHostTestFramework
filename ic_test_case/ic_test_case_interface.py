'''
Created on Aug 11, 2012

@author: gausscheng
'''

class ICTestCaseInterface(object):
    '''
    test case interface
    '''


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