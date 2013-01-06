
from ic_test.ic_tester_interface import ICTesterInterface
from ic_communicate.ic_transceiver_data import ICIMMTransceiverData


class ICParaBit(object):
    '''
    a class used for represent a test bit
    '''
    def __init__(self, index=(-1), is_on=False, delay=0):
        self.__index = index
        self.__is_on = is_on
        self.__delay = delay

    def get_index(self):
        return self.__index


    def get_is_on(self):
        return self.__is_on


    def get_delay(self):
        return self.__delay


    def set_index(self, value):
        self.__index = value


    def set_is_on(self, value):
        self.__is_on = value


    def set_delay(self, value):
        self.__delay = value


    def del_index(self):
        del self.__index


    def del_is_on(self):
        del self.__is_on


    def del_delay(self):
        del self.__delay

    index = property(get_index, set_index, del_index, "index's docstring")
    is_on = property(get_is_on, set_is_on, del_is_on, "is_on's docstring")
    delay = property(get_delay, set_delay, del_delay, "delay's docstring")


class ICParaVariable(object):
    def __init__(self, addr=0, val=0, delay=0):
        self.__addr = addr
        self.__val = val
        self.__delay = delay

    def get_addr(self):
        return self.__addr


    def get_val(self):
        return self.__val


    def get_delay(self):
        return self.__delay


    def set_addr(self, value):
        self.__addr = value


    def set_val(self, value):
        self.__val = value


    def set_delay(self, value):
        self.__delay = value


    def del_addr(self):
        del self.__addr


    def del_val(self):
        del self.__val


    def del_delay(self):
        del self.__delay

    addr = property(get_addr, set_addr, del_addr, "addr's docstring")
    val = property(get_val, set_val, del_val, "val's docstring")
    delay = property(get_delay, set_delay, del_delay, "delay's docstring")


class ICActionTestCase(object):
    '''
    a class used for represent a action test case
    '''

    def __init__(self):
        self.__name = ""
        self.__command = 0
        self.__para_sec = []
        self.__runtime_input_bits = []
        self.__runtime_variables = []
        self.__expect_output_bits = []
        self.__expect_alarm_bits = []
        self.__expect_daoutput_pressure = 0
        self.__expect_daoutput_flow = 0
        self.__expect_daoutput_bp = 0

    def get_name(self):
        return self.__name


    def get_command(self):
        return self.__command


    def get_para_sec(self):
        return self.__para_sec


    def get_runtime_input_bits(self):
        return self.__runtime_input_bits


    def get_runtime_variables(self):
        return self.__runtime_variables


    def get_expect_output_bits(self):
        return self.__expect_output_bits


    def get_expect_alarm_bits(self):
        return self.__expect_alarm_bits


    def get_expect_daoutput_pressure(self):
        return self.__expect_daoutput_pressure


    def get_expect_daoutput_flow(self):
        return self.__expect_daoutput_flow


    def get_expect_daoutput_bp(self):
        return self.__expect_daoutput_bp


    def set_name(self, value):
        self.__name = value


    def set_command(self, value):
        self.__command = value


    def set_para_sec(self, value):
        self.__para_sec = value


    def set_runtime_input_bits(self, value):
        self.__runtime_input_bits = value


    def set_runtime_variables(self, value):
        self.__runtime_variables = value


    def set_expect_output_bits(self, value):
        self.__expect_output_bits = value


    def set_expect_alarm_bits(self, value):
        self.__expect_alarm_bits = value


    def set_expect_daoutput_pressure(self, value):
        self.__expect_daoutput_pressure = value


    def set_expect_daoutput_flow(self, value):
        self.__expect_daoutput_flow = value


    def set_expect_daoutput_bp(self, value):
        self.__expect_daoutput_bp = value


    def del_name(self):
        del self.__name


    def del_command(self):
        del self.__command


    def del_para_sec(self):
        del self.__para_sec


    def del_runtime_input_bits(self):
        del self.__runtime_input_bits


    def del_runtime_variables(self):
        del self.__runtime_variables


    def del_expect_output_bits(self):
        del self.__expect_output_bits


    def del_expect_alarm_bits(self):
        del self.__expect_alarm_bits


    def del_expect_daoutput_pressure(self):
        del self.__expect_daoutput_pressure


    def del_expect_daoutput_flow(self):
        del self.__expect_daoutput_flow


    def del_expect_daoutput_bp(self):
        del self.__expect_daoutput_bp

    name = property(get_name, set_name, del_name, "name's docstring")
    command = property(get_command, set_command, del_command, "command's docstring")
    para_sec = property(get_para_sec, set_para_sec, del_para_sec, "para_sec's docstring")
    runtime_input_bits = property(get_runtime_input_bits, set_runtime_input_bits, del_runtime_input_bits, "runtime_input_bits's docstring")
    runtime_variables = property(get_runtime_variables, set_runtime_variables, del_runtime_variables, "runtime_variables's docstring")
    expect_output_bits = property(get_expect_output_bits, set_expect_output_bits, del_expect_output_bits, "expect_output_bits's docstring")
    expect_alarm_bits = property(get_expect_alarm_bits, set_expect_alarm_bits, del_expect_alarm_bits, "expect_alarm_bits's docstring")
    expect_daoutput_pressure = property(get_expect_daoutput_pressure, set_expect_daoutput_pressure, del_expect_daoutput_pressure, "expect_daoutput_pressure's docstring")
    expect_daoutput_flow = property(get_expect_daoutput_flow, set_expect_daoutput_flow, del_expect_daoutput_flow, "expect_daoutput_flow's docstring")
    expect_daoutput_bp = property(get_expect_daoutput_bp, set_expect_daoutput_bp, del_expect_daoutput_bp, "expect_daoutput_bp's docstring")



class ICActionTester(ICTesterInterface):
    '''
    class of action test case
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__name = ""
        self.__init_para_sec = []
        self.__err_code = 0
        self.__cases = []
        self.__sent_frame = ICIMMTransceiverData()
        self.__recv_frame = ICIMMTransceiverData()
        self.__test_report = ""

    def get_name(self):
        return self.__name


    def get_init_para_sec(self):
        return self.__init_para_sec


    def get_err_code(self):
        return self.__err_code


    def get_cases(self):
        return self.__cases


    def get_sent_frame(self):
        return self.__sent_frame


    def get_recv_frame(self):
        return self.__recv_frame


    def get_test_report(self):
        return self.__test_report


    def set_name(self, value):
        self.__name = value


    def set_init_para_sec(self, value):
        self.__init_para_sec = value


    def set_err_code(self, value):
        self.__err_code = value


    def set_cases(self, value):
        self.__cases = value


    def set_sent_frame(self, value):
        self.__sent_frame = value


    def set_recv_frame(self, value):
        self.__recv_frame = value


    def set_test_report(self, value):
        self.__test_report = value


    def del_name(self):
        del self.__name


    def del_init_para_sec(self):
        del self.__init_para_sec


    def del_err_code(self):
        del self.__err_code


    def del_cases(self):
        del self.__cases


    def del_sent_frame(self):
        del self.__sent_frame


    def del_recv_frame(self):
        del self.__recv_frame


    def del_test_report(self):
        del self.__test_report

    name = property(get_name, set_name, del_name, "name's docstring")
    init_para_sec = property(get_init_para_sec, set_init_para_sec, del_init_para_sec, "init_para_sec's docstring")
    err_code = property(get_err_code, set_err_code, del_err_code, "err_code's docstring")
    cases = property(get_cases, set_cases, del_cases, "cases's docstring")
    sent_frame = property(get_sent_frame, set_sent_frame, del_sent_frame, "sent_frame's docstring")
    recv_frame = property(get_recv_frame, set_recv_frame, del_recv_frame, "recv_frame's docstring")
    test_report = property(get_test_report, set_test_report, del_test_report, "test_report's docstring")
