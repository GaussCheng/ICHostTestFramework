'''
Created on Aug 11, 2012

@author: gausscheng
'''
from ic_test_case.ic_test_case_interface import ICTestCaseInterface
from xml.etree import ElementTree
from ic_communicate.ic_transceiver_data import ICIMMTransceiverData
from ic_utility.ic_timer import ICTimer

class _ICParaBit_(object):
    '''
    a class used for represent a test bit
    '''
    def __init__(self, index = -1, is_on = False, delay = 0):
        self.index = index
        self.is_on = is_on
        self.delay = delay
        
class _ICParaVariable_(object):
    def __init__(self, addr = 0, val = 0, delay = 0):
        self.addr = addr
        self.val = val
        self.delay = delay

class _ICActionTestCase_(object):
    '''
    a class used for represent a action test case
    '''
    
    def __init__(self):
        self.name = ""
        self.command = 0
        self._para_sec_ = []
        self.runtime_input_bits = []
        self.runtime_input_addr = -1
        self._runtime_variables_ = []
        self._expect_output_bits_ = []
        self._expect_alarm_bits_ = []
        self.expect_daoutput_pressure = 0
        self.expect_daoutput_flow = 0
        self.expect_daoutput_bp = 0
    
    def get_para_sec(self):
        return self._para_sec_
    
    def get_runtime_variables(self):
        return self._runtime_variables_
    
    def insert_para_(self, key, val):
        self._para_sec_[key] = val
    
    def remove_para(self, key):
        self._para_sec_.pop(key)
    
    def add_runtime_input_bit(self, index, val = -1, delay = 0):
        if val == -1:
            self.runtime_input_bits.append(index)
        else:
            self.runtime_input_bits.append(_ICParaBit_(index, val, delay))
    
    def add_expect_output_bit(self, index, val = -1, delay = 0):
        if val == -1:
            self._expect_output_bits_.append(index)
        else:
            self._expect_output_bits_.append(_ICParaBit_(index, val, delay))
        
    def add_expect_alarm_bit(self, index, val = -1, delay = 0):
        if val == -1:
            self._expect_alarm_bits_.append(index)
        else:
            self._expect_alarm_bits_.append(_ICParaBit_(index, val, delay))

class ICActionTestCase(ICTestCaseInterface):
    '''
    class of action test case
    '''


    ACTION_COMMAND_ADDR         = 2

    ACTION_ROOT_STR             = "action"
    ACTION_INIT_PARA_SEC_STR    = "init_para_sec"
    ACTION_PARA_SEC_STR         = "para_sec"
    ACTION_PARA_STR             = "addr"
    ACTION_PARA_ADDR_STR        = "key"
    ACTION_NAME_STR             = "name"
    ACTION_CASE_STR             = "case"
    ACTION_CASE_NAME_STR        = "name"
    ACTION_CASE_COMMAND_STR     = "command"
    ACTION_CASE_RUNTIME_STR     = "runtime_status"
    ACTION_CASE_EXPECT_STR      = "expect"
    ACTION_CASE_INPUT_STR       = "input"
    ACTION_CASE_OUTPUT_STR      = "output"
    ACTION_CASE_ALARM_STR       = "alarm"
    ACTION_CASE_DAOUTPUT_STR    = "da_output"  
    PARA_BIT_STR                = "bit"
    PARA_BIT_INDEX_STR          = "index"
    DELAY_STR                   = "delay"
    RUNTIME_VARIABLE_STR        = "status_varialbes"
    RUNTIME_INPUT_ADDR_STR      = "addr"
    
    ERR_ACTION_CASE_ROOT_NAME       = 1
    ERR_ACTION_CASE_PARA_NULL_ADDR  = 2
    ERR_ACTION_CASE_PARA_TYPE       = 3
    ERR_ACTION_CASE_VAL_TYPE        = 4
    ERR_ACTION_CASE_COMMAND_TYPE    = 5
    ERR_PARA_BIT_NO_INDEX           = 6
    ERR_PARA_BIT_INDEX_TYPE         = 7
    ERR_DELAY_TYPE                  = 8
    ERR_PARA_BIT_VAL_TYPE           = 9
    ERR_DAOUTPUT_PARA_VAL_TYPE      = 10
    ERR_RUNTIME_INPUT_ADDR_INVALID  = 11
    
    COMMUNICATE_FAIL                = 50
    
    def __init__(self):
        '''
        Constructor
        '''
        self.name = ""
        self._init_para_sec_ = [] 
        self._err_code_ = 0
        self._cases_    = []
        self.sent_frame = ICIMMTransceiverData()
        self.recv_frame = ICIMMTransceiverData()
        self._test_report_ = ""
        
    def err_code(self):
        return self._err_code_
    
    def case_name(self):
        return self.name
    
    def test_report(self):
        return self._test_report_
    
    def run_case(self):
        self.sent_frame.function_code = ICIMMTransceiverData.FUNCTION_CODE_WRITE
        self.sent_frame.data_buffer = []
        self.sent_frame.data_buffer.append(0)
        self.sent_frame.length = 1
        recv_status = False
        self._test_report_ = ""
        self._test_report_ += self.case_name() + ": test start\n"
        for para in self._init_para_sec_:
            self.sent_frame.addr = para.addr
            self.sent_frame.data_buffer[0] = para.val
            recv_status = self.sent_frame.communicate(self.recv_frame, self.g_serial_transceiver)
            if recv_status == False:
                self.communicate_fail_report("", "init", self.sent_frame, self.recv_frame)
                self._test_report_ += self.case_name() + ": test end"
                return False
        
        case_para_sec = []
        for case in self._cases_:
            self._test_report_ += "    " + case.name + ": test start\n"
            case_para_sec = case.get_para_sec()
            for para in case_para_sec:          #Send the parameters of case to host
                self.sent_frame.addr = para.addr
                self.sent_frame.length = 1
                self.sent_frame.data_buffer[0] = para.val
                recv_status = self.sent_frame.communicate(self.recv_frame, self.g_serial_transceiver)
                if recv_status == False:
                    self.communicate_fail_report("    ", "set para", self.sent_frame, self.recv_frame)
                    self._test_report_ +=  "    " + case.name + ": test end"
                    break
            else:
                self.sent_frame.addr = self.ACTION_COMMAND_ADDR
                self.sent_frame.data_buffer[0] = case.command
                if recv_status == False:
                    self.communicate_fail_report("    ", "set command", self.sent_frame, self.recv_frame)
                    continue
                timer = ICTimer()
                timer.start()
                timer_eplased = 0
                case_runtime_vars = case.get_runtime_variables()[:]
                case_runtime_input_bits = case.runtime_input_bits[:]
                set_input_bits = 0
                case_expect_output_bits = self._expect_output_bits_[:]
                case_expect_alarm_bits = self._expect_alarm_bits_[:]
                while(True):
                    #set input
                    is_input_bits_changed = False
                    for input_bit in case_runtime_input_bits[:]:
                        timer_eplased = timer.elapsed()
                        if timer_eplased >= input_bit.delay:
                            is_input_bits_changed = True
                            if input_bit.is_on:
                                set_input_bits |= 1 << input_bit.index
                            else: set_input_bits &= 1 << input_bit.index
                            case_runtime_input_bits.remove(input_bit)
                    
                    self.sent_frame.function_code = ICIMMTransceiverData.FUNCTION_CODE_DEBUG_WRITE
                    self.sent_frame.length = 1
                    if is_input_bits_changed:
                        self.sent_frame.addr = case.runtime_input_addr
                        self.sent_frame.data_buffer[0] = set_input_bits
                        recv_status = self.sent_frame.communicate(self.recv_frame, self.g_serial_transceiver)
                        if recv_status == False:
                            self.communicate_fail_report("    ", "set runtime input", self.sent_frame, self.recv_frame)
                            break
                    
                    #set runtime variable
                    for rt_var in case_runtime_vars[:]:
                        timer_eplased = timer.elapsed()
                        if timer_eplased >= rt_var.delay:
                            self.sent_frame.addr = rt_var.addr
                            self.sent_frame.data_buffer[0] = rt_var.val
                            recv_status = self.sent_frame.communicate(self.recv_frame, self.g_serial_transceiver)
                            if recv_status == False:
                                self.communicate_fail_report("    ", "set runtime variables", self.sent_frame, self.recv_frame)
                                break
                            case_runtime_vars.remove(rt_var)
                    
                    #check expect
                    does_need_check_output = False
                    for ep_out in case_expect_output_bits:
                        timer_eplased = timer.elapsed()
                        if timer_eplased >= ep_out.delay:
                            does_need_check_output = True
                    self.sent_frame.function_code = ICIMMTransceiverData.FUNCTION_CODE_READ
                    if does_need_check_output:
                        self.sent_frame.addr = ICIMMTransceiverData.READ_OUTPUT_ADDR
                        self.sent_frame.length = 2
                        
                    #check if we should stop
                    
                 
                
            
                
        self._test_report_ += self.case_name() + ": test end"
        return str(self.err_code()) + str(len(self._cases_))
        
    def load(self, str_content):
        root = ElementTree.fromstring(str_content)
        if root.tag != self.ACTION_ROOT_STR:
            self._err_code_ = self.ERR_ACTION_CASE_ROOT_NAME
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
                self._err_code_ = self.ERR_ACTION_CASE_COMMAND_TYPE
                return False
            case.command = int(tmp.text)
        tmp = node.find(self.ACTION_CASE_RUNTIME_STR)
        if tmp != None:
            runtime_s = tmp.find(self.ACTION_CASE_INPUT_STR)
            if runtime_s != None:
                input_addr = runtime_s.get(self.RUNTIME_INPUT_ADDR_STR)
                if input_addr == None:
                    self._err_code_ = self.ERR_RUNTIME_INPUT_ADDR_INVALID
                    return False
                if not input_addr.isdecimal():
                    self._err_code_ = self.ERR_RUNTIME_INPUT_ADDR_INVALID
                    return False
                case.runtime_input_addr = int(input_addr)
                bits = runtime_s.iter(self.PARA_BIT_STR)
                for bit in bits:
                    pb = self._parse_para_bits(bit)
                    if self.err_code() == 0:
                        case.add_runtime_input_bit(pb)
                    else: return False
                    
            runtime_s = tmp.find(self.RUNTIME_VARIABLE_STR)
            if runtime_s != None:
                self._parse_para_sec_(runtime_s, case.get_runtime_variables())
        
        tmp = node.find(self.ACTION_CASE_EXPECT_STR)
        if tmp == None:
            return True
                    
        expect = tmp.find(self.ACTION_CASE_OUTPUT_STR)
        if expect != None:
            bits = expect.iter(self.PARA_BIT_STR)
            for bit in bits:
                pb = self._parse_para_bits(bit)
                if self.err_code() == 0:
                    case.add_expect_output_bit(pb)
                else: return False
        
        expect = tmp.find(self.ACTION_CASE_ALARM_STR)
        if expect != None:
            bits = expect.iter(self.PARA_BIT_STR)
            for bit in bits:
                pb = self._parse_para_bits(bit)
                if self.err_code() == 0:
                    case.add_expect_alarm_bit(pb)
                else: return False
        
        expect = tmp.find(self.ACTION_CASE_DAOUTPUT_STR)
        if expect != None:
            tmp = expect.find("pressure")
            if tmp != None:
                if tmp.text == None:
                    self._err_code_ = self.ERR_DAOUTPUT_PARA_VAL_TYPE
                    return False
                elif not tmp.text.isdecimal():
                    self._err_code_ = self.ERR_DAOUTPUT_PARA_VAL_TYPE
                    return False
                case.expect_daoutput_pressure = int(tmp.text)
            tmp = expect.find("flow")
            if tmp != None:
                if tmp.text == None:
                    self._err_code_ = self.ERR_DAOUTPUT_PARA_VAL_TYPE
                    return False
                elif not tmp.text.isdecimal():
                    self._err_code_ = self.ERR_DAOUTPUT_PARA_VAL_TYPE
                    return False
                case.expect_daoutput_flow = int(tmp.text)
            tmp = expect.find("back_pressure")
            if tmp != None:
                if tmp.text == None:
                    self._err_code_ = self.ERR_DAOUTPUT_PARA_VAL_TYPE
                    return False
                elif not tmp.text.isdecimal():
                    self._err_code_ = self.ERR_DAOUTPUT_PARA_VAL_TYPE
                    return False
                case.expect_daoutput_bp = (int)(tmp.text)
        return True
               
    def _parse_para_bits(self, node):
        para_bit = _ICParaBit_()
        tmp = node.get(self.PARA_BIT_INDEX_STR)
        if tmp == None:
            self._err_code_ = self.ERR_PARA_BIT_NO_INDEX
            return para_bit
        if not tmp.isdecimal():
            self._err_code_ = self.ERR_PARA_BIT_INDEX_TYPE
            return para_bit
        para_bit.index = int(tmp)
        tmp = node.get(self.DELAY_STR)
        if tmp != None:
            if not tmp.isdecimal():
                self._err_code_ = self.ERR_DELAY_TYPE
                return para_bit
            para_bit.delay = int(tmp)
        tmp = node.text
        if not tmp.isdecimal:
            self._err_code_ = self.ERR_PARA_BIT_VAL_TYPE
            return para_bit
        para_bit.is_on = int(tmp) > 0
        return para_bit
        
    def _parse_para_sec_(self, node, para_sec):
        node = node.iter(self.ACTION_PARA_STR)
        para_addr = 0
        para_val = 0
        para_delay = 0
        for para in node:
            para_addr = para.get(self.ACTION_PARA_ADDR_STR)
            if para_addr == None:
                self._err_code_ = self.ERR_ACTION_CASE_PARA_NULL_ADDR
                return False
            if not para_addr.isdecimal():
                self._err_code_ = self.ERR_ACTION_CASE_PARA_TYPE
                return False
            para_val = para.text
            if not para_val.isdecimal():
                self._err_code_ = self.ERR_ACTION_CASE_VAL_TYPE
                return False
            para_delay = para.get(self.DELAY_STR)
            if para_delay != None:
                if not para_delay.isdecimal():
                    self._err_code_ = self.ERR_DELAY_TYPE
                    return False
            else: para_delay = 0
            para_sec.append(_ICParaVariable_(int(para_addr), int(para_val), int(para_delay)))
        return True
       
    def communicate_fail_report(self, sep, condition, sent_frame, recv_frame):
        self._err_code_ = self.COMMUNICATE_FAIL
        self._test_report_ += sep + "Communicate fail when " + condition + "!\n"
        self._test_report_ += sep + "    sent:" + sent_frame.tostring(ICIMMTransceiverData.DECIMAL_FORMAT) + " \n"
        self._test_report_ += sep + "    recv:" + recv_frame.tostring(ICIMMTransceiverData.DECIMAL_FORMAT) + " \n"  
            