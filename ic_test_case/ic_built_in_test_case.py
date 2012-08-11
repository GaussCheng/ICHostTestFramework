'''
Created on Aug 11, 2012

@author: gausscheng
'''
from ic_test_case.ic_test_case_interface import ICTestCaseInterface
from xml.etree import ElementTree

class _ICParaBit_(object):
    '''
    a class used for represent a test bit
    '''
    def __init__(self, index = -1, is_on = False, delay = 0):
        self.index = index
        self.is_on = is_on
        self.delay = delay

class _ICActionTestCase_(object):
    '''
    a class used for represent a action test case
    '''
    
    def __init__(self):
        self.name = ""
        self.command = 0
        self._para_sec_ = {}
        self._expect_input_bits_ = []
        self._expect_output_bits_ = []
        self._expect_alarm_bits_ = []
        self.expect_daoutput_pressure = 0
        self.expect_daoutput_flow = 0
        self.expect_daoutput_bp = 0
    
    def get_para_sec(self):
        return self._para_sec_
    
    def insert_para_(self, key, val):
        self._para_sec_[key] = val
    
    def remove_para(self, key):
        self._para_sec_.pop(key)
    
    def add_expect_input_bit(self, index, val, delay = 0):
        self._expect_input_bits_.append(_ICParaBit_(index, val, delay))
    def add_expect_intput_bit(self, para_bit):
        self._expect_input_bits_.append(para_bit)
    
    def add_expect_output_bit(self, index, val, delay = 0):
        self._expect_output_bits_.append(_ICParaBit_(index, val, delay))
        
    def add_alarm_bit(self, index, val, delay = 0):
        self._expect_alarm_bits_.append(_ICParaBit_(index, val, delay))

class ICActionTestCase(ICTestCaseInterface):
    '''
    class of action test case
    '''


    ACTION_ROOT_STR             = "action"
    ACTION_INIT_PARA_SEC_STR    = "init_para_sec"
    ACTION_PARA_SEC_STR         = "para_sec"
    ACTION_PARA_STR             = "addr"
    ACTION_PARA_ADDR_STR        = "key"
    ACTION_NAME_STR             = "name"
    ACTION_CASE_STR             = "case"
    ACTION_CASE_NAME_STR        = "name"
    ACTION_CASE_COMMAND_STR     = "command"
    ACTION_CASE_EXPECT_STR      = "expect"
    ACTION_CASE_INPUT_STR       = "input"
    ACTION_CASE_OUTPUT_STR      = "output"
    ACTION_CASE_ALARM_STR       = "alarm"
    ACTION_CASE_DAOUTPUT_STR    = "da_output"  
    PARA_BIT_STR                = "bit"
    PARA_BIT_INDEX_STR          = "index"
    PARA_BIT_DELAY_STR          = "delay"
    
    ACTION_CASE_ERR_ROOT_NAME       = 1
    ACTION_CASE_ERR_PARA_NULL_ADDR  = 2
    ACTION_CASE_ERR_PARA_TYPE       = 3
    ACTION_CASE_ERR_VAL_TYPE        = 4
    ACTION_CASE_ERR_COMMAND_TYPE    = 5
    PARA_BIT_ERR_NO_INDEX           = 6
    PARA_BIT_ERR_INDEX_TYPE         = 7
    PARA_BIT_ERR_DELAY_TYPE         = 8
    PARA_BIT_ERR_VAL_TYPE           = 9
    
    def __init__(self):
        '''
        Constructor
        '''
        self.name = ""
        self._init_para_sec_ = {} 
        self._err_code_ = 0
        self._cases_    = []
        
    def err_code(self):
        return self._err_code_
    
    def case_name(self):
        return self.name
    
    def run_case(self):
        return len(self._cases_)
        
    def load(self, str_content):
        root = ElementTree.fromstring(str_content)
        if root.tag != self.ACTION_ROOT_STR:
            self._err_code_ = self.ACTION_CASE_ERR_ROOT_NAME
            return False
        node = root.find(self.ACTION_INIT_PARA_SEC_STR)
        if node != None:
            self._parse_para_sec_(node, self._init_para_sec_)
        
        node = root.find(self.ACTION_CASE_NAME_STR)
        if node != None:
            self.name = node.text
        cases = root.iter(self.ACTION_CASE_STR)
        for case in cases:
            tmp_case = _ICActionTestCase_()
            self._parse_case_sec(case, tmp_case)
            if self.err_code() == 0:
                self._cases_.append(tmp_case)
        return True
        
    def _parse_case_sec(self, node, case):
        para_sec = node.find(self.ACTION_PARA_SEC_STR)
        if para_sec != None:
            self._parse_para_sec_(node, case.get_para_sec())
        tmp = node.find(self.ACTION_CASE_NAME_STR)
        if tmp != None:
            case.name = tmp.text
        tmp = node.find(self.ACTION_CASE_COMMAND_STR)
        if tmp != None:
            if not tmp.text.isdecimal():
                self._err_code_ = self.ACTION_CASE_ERR_COMMAND_TYPE
                return False
            case.command = int(tmp.text)
        tmp = node.find(self.ACTION_CASE_EXPECT_STR)
        if tmp == None:
            return True
        
        expect = tmp.find(self.ACTION_CASE_INPUT_STR)
        if expect != None:
            bits = expect.iter(self.PARA_BIT_STR)
            for bit in bits:
                pb = self._parse_para_bits(bit)
                if self.err_code() == 0:
                    case.add_expect_input_bit(pb)
                else: return False
                    
        expect = node.find(self.ACTION_CASE_OUTPUT_STR)
        if expect != None:
            bits = expect.iter(self.PARA_BIT_STR)
            for bit in bits:
                pb = self._parse_para_bits(bit)
                if self.err_code() == 0:
                    case.add_expect_output_bit(pb)
                else: return False
        
        expect = node.find(self.ACTION_CASE_ALARM_STR)
        if expect != None:
            bits = expect.iter(self.PARA_BIT_STR)
            for bit in bits:
                pb = self._parse_para_bits(bit)
                if self.err_code() == 0:
                    case.add_expect_alarm_bit(pb)
                else: return False
        
        expect = node.find(self.ACTION_CASE_DAOUTPUT_STR)
        if expect != None:
            tmp = expect.find("pressure")
            if tmp != None:
                case.expect_daoutput_pressure = int(tmp.text)
            tmp = expect.find("flow")
            if tmp != None:
                case.expect_daoutput_flow = int(tmp.text)
            tmp = expect.find("back_pressure")
            if tmp != None:
                case.expect_daoutput_bp = (int)(tmp.text)
        return True
            
        
        
    def _parse_para_bits(self, node):
        para_bit = _ICParaBit_()
        tmp = node.get(self.PARA_BIT_INDEX_STR)
        if tmp == None:
            self._err_code_ = self.PARA_BIT_ERR_NO_INDEX
            return para_bit
        if not tmp.isdecimal():
            self._err_code_ = self.PARA_BIT_ERR_INDEX_TYPE
            return para_bit
        para_bit.index = int(tmp)
        tmp = node.get(self.PARA_BIT_DELAY_STR)
        if tmp != None:
            if not tmp.isdecimal():
                self._err_code_ = self.PARA_BIT_ERR_DELAY_TYPE
                return para_bit
            para_bit.delay = int(tmp)
        tmp = node.text
        if not tmp.isdecimal:
            self._err_code_ = self.PARA_BIT_ERR_VAL_TYPE
            return para_bit
        para_bit.is_on = int(tmp) > 0
        return para_bit
        
    def _parse_para_sec_(self, node, sec_dict):
        node = node.iter(self.ACTION_PARA_STR)
        para_addr = ""
        para_val = ""
        for para in node:
            para_addr = para.get(self.ACTION_PARA_ADDR_STR)
            if para_addr == None:
                self._err_code_ = self.ACTION_CASE_ERR_PARA_NULL_ADDR
                return False
            if not para_addr.isdecimal():
                self._err_code_ = self.ACTION_CASE_ERR_PARA_TYPE
                return False
            para_val = para.text
            if not para_val.isdecimal():
                self._err_code_ = self.ACTION_CASE_ERR_VAL_TYPE
                return False
            sec_dict[int(para_addr)] = int(para_val)
        return True
            
            
            
            