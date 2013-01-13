
import yaml
from ic_test.ic_tester_interface import ICTesterInterface, YamlType
from ic_test.ic_tester_interface import get_value_from_hash_helper
from ic_communicate.ic_transceiver_data import ICIMMTransceiverData


class ICParaBit(YamlType):
    '''
    a class used for represent a test bit
    '''

    BIT_TAG = "bit"
    BIT_INDEX_TAG = "index"
    BIT_DELAY_TAG = "delay"
    BIT_VALUE_TAG = "value"

    def __init__(self, index=(-1), is_on=False, delay=0, value_hash=None):
        self.__index = index
        self.__is_on = is_on
        self.__delay = delay
        if value_hash != None:
            self.get_value_from_hash(value_hash)

    def __repr__(self):
        return "%s(index=%r, is_on=%r, delay=%r)" % (
                self.__class__.__name__, self.index, self.is_on, self.delay)

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

    def to_hash(self):
        return {self.BIT_TAG: {self.BIT_INDEX_TAG: self.index,
                self.BIT_DELAY_TAG: self.delay,
                self.BIT_VALUE_TAG: self.is_on}}

    def get_value_from_hash(self, value_hash):
        if self.BIT_TAG in value_hash:
            bit_hash = value_hash[self.BIT_TAG]
            self.index = get_value_from_hash_helper(self.BIT_INDEX_TAG,
                                                    bit_hash,
                                                    (-1))
            self.delay = get_value_from_hash_helper(self.BIT_DELAY_TAG,
                                                    bit_hash,
                                                    0)
            self.is_on = get_value_from_hash_helper(self.BIT_VALUE_TAG,
                                                    bit_hash,
                                                    False)


class ICParaVariable(YamlType):

    VARIABLE_TAG = "variable"
    VARIABLE_ADDR_TAG = "addr"
    VARIABLE_VALUE_TAG = "value"
    VARIABLE_DELAY_TAG = "delay"

    def __init__(self, addr=0, val=0, delay=0, value_hash=None):
        self.__addr = addr
        self.__value = val
        self.__delay = delay
        if value_hash != None:
            self.get_value_from_hash(value_hash)

    def __repr__(self):
        return "%s(addr=%r, value=%r, delay=%r)" % (
                self.__class__.__name__, self.addr, self.value, self.delay)

    def get_addr(self):
        return self.__addr

    def get_value(self):
        return self.__value

    def get_delay(self):
        return self.__delay

    def set_addr(self, value):
        self.__addr = value

    def set_value(self, value):
        self.__value = value

    def set_delay(self, value):
        self.__delay = value

    def del_addr(self):
        del self.__addr

    def del_value(self):
        del self.__value

    def del_delay(self):
        del self.__delay

    addr = property(get_addr, set_addr, del_addr, "addr's docstring")
    value = property(get_value, set_value, del_value, "value's docstring")
    delay = property(get_delay, set_delay, del_delay, "delay's docstring")

    def to_hash(self):
        return {self.VARIABLE_TAG: {self.VARIABLE_ADDR_TAG: self.addr,
                self.VARIABLE_DELAY_TAG: self.delay,
                self.VARIABLE_VALUE_TAG: self.value}}

    def get_value_from_hash(self, value_hash):
        if self.VARIABLE_TAG in value_hash:
            variable_hash = value_hash[self.VARIABLE_TAG]
            self.addr = get_value_from_hash_helper(self.VARIABLE_ADDR_TAG,
                                                    variable_hash,
                                                    0)
            self.delay = get_value_from_hash_helper(self.VARIABLE_DELAY_TAG,
                                                    variable_hash,
                                                    0)
            self.value = get_value_from_hash_helper(self.VARIABLE_VALUE_TAG,
                                                    variable_hash,
                                                    0)


class ICActionCaseRuntimeStatus(YamlType):

    RUNTIME_STATUS_TAG = "runtime_status"
    RUNTIME_STATUS_INPUT_BITS_TAG = "input_bits"
    RUNTIME_STATUS_STATUS_VARIABLES_TAG = "status_variables"

    def __init__(self, value_hash=None):
        if value_hash == None:
            self.__input_bits = []
            self.__status_variables = []
        else:
            self.get_value_from_hash(value_hash)

    def __repr__(self):
        return """%s(
                    input_bits=%r,
                    status_variables=%r)""" % (
                    self.__class__.__name__,
                    self.input_bits,
                    self.status_variables)

    def get_input_bits(self):
        return self.__input_bits

    def get_status_variables(self):
        return self.__status_variables

    def set_input_bits(self, value):
        self.__input_bits = value

    def set_status_variables(self, value):
        self.__status_variables = value

    def del_input_bits(self):
        del self.__input_bits

    def del_status_variables(self):
        del self.__status_variables

    input_bits = property(get_input_bits,
                          set_input_bits,
                          del_input_bits,
                          "input_bits's docstring")
    status_variables = property(get_status_variables,
                                set_status_variables,
                                del_status_variables,
                                "status_variables's docstring")

    def to_hash(self):
        return {self.RUNTIME_STATUS_TAG: {
            self.RUNTIME_STATUS_INPUT_BITS_TAG:
                            [x.to_hash() for x in self.input_bits],
            self.RUNTIME_STATUS_STATUS_VARIABLES_TAG:
                            [x.to_hash() for x in self.status_variables]}}

    def get_value_from_hash(self, value_hash):
        if self.RUNTIME_STATUS_TAG in value_hash:
            runtime_status_hash = value_hash[self.RUNTIME_STATUS_TAG]
            if self.RUNTIME_STATUS_INPUT_BITS_TAG in runtime_status_hash:
                self.input_bits = [ICParaBit(value_hash=x)
                                   for x in runtime_status_hash[
                                        self.RUNTIME_STATUS_INPUT_BITS_TAG]]
            if self.RUNTIME_STATUS_STATUS_VARIABLES_TAG in runtime_status_hash:
                self.status_variables = [ICParaVariable(value_hash=x)
                                         for x in runtime_status_hash[
                                    self.RUNTIME_STATUS_STATUS_VARIABLES_TAG]]


class ICDAOutput(YamlType):

    DAOUTPUT_TAG = "da_output"
    DAOUTPUT_PRESSURE_TAG = "pressure"
    DAOUTPUT_FLOW_TAG = "flow"
    DAOUTPUT_BACK_PRESSURE_TAG = "back_pressure"

    def __init__(self, value_hash=None):
        self.__pressure = 0
        self.__flow = 0
        self.__back_pressure = 0
        if value_hash != None:
            self.get_value_from_hash(value_hash)

    def __repr__(self):
        return """%s(
                        pressure=%r,
                        flow=%r,
                        back_pressure=%r)""" % (
                        self.__class__.__name__,
                        self.pressure,
                        self.flow,
                        self.back_pressure)

    def get_pressure(self):
        return self.__pressure

    def get_flow(self):
        return self.__flow

    def get_back_pressure(self):
        return self.__back_pressure

    def set_pressure(self, value):
        self.__pressure = value

    def set_flow(self, value):
        self.__flow = value

    def set_back_pressure(self, value):
        self.__back_pressure = value

    def del_pressure(self):
        del self.__pressure

    def del_flow(self):
        del self.__flow

    def del_back_pressure(self):
        del self.__back_pressure

    pressure = property(get_pressure,
                        set_pressure,
                        del_pressure,
                        "pressure's docstring")
    flow = property(get_flow, set_flow, del_flow, "flow's docstring")
    back_pressure = property(get_back_pressure,
                             set_back_pressure,
                             del_back_pressure,
                             "back_pressure's docstring")

    def to_hash(self):
        return {self.DAOUTPUT_TAG: {self.DAOUTPUT_PRESSURE_TAG: self.pressure,
                self.DAOUTPUT_BACK_PRESSURE_TAG: self.back_pressure,
                self.DAOUTPUT_FLOW_TAG: self.flow}}

    def get_value_from_hash(self, value_hash):
        if self.DAOUTPUT_TAG in value_hash:
            da_output_hash = value_hash[self.DAOUTPUT_TAG]
            self.pressure = get_value_from_hash_helper(
                                                    self.DAOUTPUT_PRESSURE_TAG,
                                                    da_output_hash,
                                                    0)
            self.back_pressure = get_value_from_hash_helper(
                                            self.DAOUTPUT_BACK_PRESSURE_TAG,
                                            da_output_hash,
                                            0)
            self.flow = get_value_from_hash_helper(self.DAOUTPUT_FLOW_TAG,
                                                    da_output_hash,
                                                    0)


class ICActionCaseExpected(YamlType):

    EXPECTED_TAG = "expected"
    EXPECTED_OUTPUT_BITS = "output_bits"
    EXPECTED_DAOUTPUT = "da_output"
    EXPECTED_ALARMS = "alarms"

    def __init__(self, value_hash=None):
        if value_hash == None:
            self.__output_bits = []
            self.__da_ouputs = ICDAOutput()
            self.__alarm_bits = []
        else:
            self.get_value_from_hash(value_hash)

    def __repr__(self):
        return """%s(
                    output_bits=%r,
                    da_output=%r,
                    alarm=%r)""" % (
                    self.__class__.__name__,
                    self.output_bits,
                    self.da_ouputs,
                    self.alarm_bits)

    def get_output_bits(self):
        return self.__output_bits

    def get_da_ouputs(self):
        return self.__da_ouputs

    def get_alarm_bits(self):
        return self.__alarm_bits

    def set_output_bits(self, value):
        self.__output_bits = value

    def set_da_ouputs(self, value):
        self.__da_ouputs = value

    def set_alarm_bits(self, value):
        self.__alarm_bits = value

    def del_output_bits(self):
        del self.__output_bits

    def del_da_ouputs(self):
        del self.__da_ouputs

    def del_alarm_bits(self):
        del self.__alarm_bits

    output_bits = property(get_output_bits,
                           set_output_bits,
                           del_output_bits,
                           "output_bits's docstring")
    da_ouputs = property(get_da_ouputs,
                         set_da_ouputs,
                         del_da_ouputs,
                         "da_ouputs's docstring")
    alarm_bits = property(get_alarm_bits,
                          set_alarm_bits,
                          del_alarm_bits,
                          "alarm_bits's docstring")

    def to_hash(self):
        return {self.EXPECTED_TAG: {self.EXPECTED_OUTPUT_BITS: [x.to_hash()
                                            for x in self.output_bits]},
                self.EXPECTED_DAOUTPUT: self.da_ouputs.to_hash(),
                self.EXPECTED_ALARMS: [x.to_hash()
                                       for x in self.alarm_bits]}

    def get_value_from_hash(self, value_hash):
        if self.EXPECTED_TAG in value_hash:
            expected_hash = value_hash[self.EXPECTED_TAG]
            if self.EXPECTED_OUTPUT_BITS in expected_hash:
                self.output_bits = [ICParaBit(value_hash=x)
                            for x in expected_hash[self.EXPECTED_OUTPUT_BITS]]
            if self.EXPECTED_DAOUTPUT in expected_hash:
                self.da_ouputs = ICDAOutput(expected_hash)
            if self.EXPECTED_ALARMS in expected_hash:
                self.alarm_bits = [ICParaBit(value_hash=x)
                                for x in expected_hash[self.EXPECTED_ALARMS]]


class ICActionTestCase(YamlType):
    '''
    a class used for represent a action test case
    '''

    CASE_TAG = "case"
    CASE_NAME_TAG = "name"
    CASE_PARA_SEC_TAG = "para_sec"
    CASE_COMMAND_TAG = "command"
    CASE_RUNTIME_STATUS_TAG = "runtime_status"
    CASE_EXPECTED_TAG = "expected"

    def __init__(self, value_hash=None):
        self.__runtime_status = ICActionCaseRuntimeStatus()
        self.__case_expected = ICActionCaseExpected()
        if value_hash == None:
            self.__name = ""
            self.__command = 0
            self.__para_sec = {}
        else:
            self.get_value_from_hash(value_hash)

    def __repr__(self):
        return """%s(
                name=%r,
                para_sec=%r,
                command=%r,
                runtime_status=%r,
                expected=%r)""" % (
                self.__class__.__name__,
                self.name,
                self.para_sec,
                self.command,
                self.runtime_status,
                self.case_expected)

    def get_name(self):
        return self.__name

    def get_command(self):
        return self.__command

    def get_para_sec(self):
        return self.__para_sec

    def get_runtime_status(self):
        return self.__runtime_status

    def get_case_expected(self):
        return self.__case_expected

    def set_name(self, value):
        self.__name = value

    def set_command(self, value):
        self.__command = value

    def set_para_sec(self, value):
        self.__para_sec = value

    def set_runtime_status(self, value):
        self.__runtime_status = value

    def set_case_expected(self, value):
        self.__case_expected = value

    def del_name(self):
        del self.__name

    def del_command(self):
        del self.__command

    def del_para_sec(self):
        del self.__para_sec

    def del_runtime_status(self):
        del self.__runtime_status

    def del_case_expected(self):
        del self.__case_expected

    name = property(get_name,
                    set_name,
                    del_name,
                    "name's docstring")
    command = property(get_command,
                       set_command,
                       del_command,
                       "command's docstring")
    para_sec = property(get_para_sec,
                        set_para_sec,
                        del_para_sec,
                        "para_sec's docstring")
    runtime_status = property(get_runtime_status,
                              set_runtime_status,
                              del_runtime_status,
                              "runtime_status's docstring")
    case_expected = property(get_case_expected,
                             set_case_expected,
                             del_case_expected,
                             "case_expected's docstring")

    def to_hash(self):
        runtime_status_hash = self.runtime_status.to_hash()
        case_expected_hash = self.case_expected.to_hash()
        return {self.CASE_TAG: {self.CASE_NAME_TAG: self.name,
                self.CASE_PARA_SEC_TAG: self.para_sec,
                self.CASE_COMMAND_TAG: self.command,
                self.CASE_RUNTIME_STATUS_TAG:
                        runtime_status_hash[self.CASE_RUNTIME_STATUS_TAG],
                self.CASE_EXPECTED_TAG:
                        case_expected_hash[self.CASE_EXPECTED_TAG]}}

    def get_value_from_hash(self, value_hash):
        if self.CASE_TAG in value_hash:
            case_hash = value_hash[self.CASE_TAG]
            self.name = get_value_from_hash_helper(self.CASE_NAME_TAG,
                                                   case_hash,
                                                   "")
            self.para_sec = get_value_from_hash_helper(self.CASE_PARA_SEC_TAG,
                                                       case_hash,
                                                       {})
            self.command = get_value_from_hash_helper(self.CASE_COMMAND_TAG,
                                                      case_hash,
                                                      0)
            if self.CASE_RUNTIME_STATUS_TAG in case_hash:
                self.runtime_status.get_value_from_hash(case_hash)
            if self.CASE_EXPECTED_TAG in case_hash:
                self.case_expected.get_value_from_hash(case_hash)


class ICActionTester(ICTesterInterface):
    '''
    class of action test case
    '''

    ACTION_TAG = "action"
    ACTION_NAME_TAG = "name"
    ACTION_INIT_PARA_SEC_TAG = "init_para_sec"
    ACTION_CASES_TAG = "cases"

    def __init__(self, value_hash=None):
        self.__err_code = 0
        self.__sent_frame = ICIMMTransceiverData()
        self.__recv_frame = ICIMMTransceiverData()
        self.__test_report = ""
        if value_hash == None:
            self.__name = ""
            self.__init_para_sec = {}
            self.__cases = []
        else:
            self.get_value_from_hash(value_hash)

    def __repr__(self):
        return """%s(
            name=%r,
            init_para_sec=%r,
            cases=%r)""" % (
            self.__class__.__name__,
            self.name,
            self.init_para_sec, self.cases)

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

    name = property(get_name,
                    set_name,
                    del_name,
                    "name's docstring")
    init_para_sec = property(get_init_para_sec,
                             set_init_para_sec,
                             del_init_para_sec,
                             "init_para_sec's docstring")
    err_code = property(get_err_code,
                        set_err_code,
                        del_err_code,
                        "err_code's docstring")
    cases = property(get_cases, set_cases, del_cases, "cases's docstring")
    sent_frame = property(get_sent_frame,
                          set_sent_frame,
                          del_sent_frame,
                          "sent_frame's docstring")
    recv_frame = property(get_recv_frame,
                          set_recv_frame,
                          del_recv_frame,
                          "recv_frame's docstring")
    test_report = property(get_test_report,
                           set_test_report,
                           del_test_report,
                           "test_report's docstring")

    def to_hash(self):
        return {self.ACTION_TAG: {
                        self.ACTION_NAME_TAG: self.name,
                        self.ACTION_INIT_PARA_SEC_TAG: self.init_para_sec,
                        self.ACTION_CASES_TAG:
                        [x.to_hash() for x in self.cases]}}

    def get_value_from_hash(self, value_hash):
        if self.ACTION_TAG in value_hash:
            action_hash = value_hash[self.ACTION_TAG]
            self.name = get_value_from_hash_helper(self.ACTION_NAME_TAG,
                                       action_hash,
                                       "")
            self.init_para_sec = get_value_from_hash_helper(
                                       self.ACTION_INIT_PARA_SEC_TAG,
                                       action_hash,
                                       {})
            if self.ACTION_CASES_TAG in action_hash:
                self.cases = [ICActionTestCase(x)
                              for x in action_hash[self.ACTION_CASES_TAG]]
                
    def load(self, str_content):
        return self.get_value_from_hash(yaml.load(str_content))

    def case_name(self):
        return self.name

    def run_case(self):
        return self.case_name() + "test fail!"

    def err_code(self):
        return 0

    def err_descr(self):
        return ""

    def test_report(self):
        return ""


if __name__ == '__main__':
    action_tester = ICActionTester(yaml.load(
        """

        action:
          name: Close Mold

          init_para_sec:
            1: 1
            2: 2
            3: 3

          cases:
            - case:
                  name: Test close mold action
                  para_sec:
                      1: 1
                      2: 2
                      3: 3
                  command: 5
                  runtime_status:
                    input_bits:
                      - bit:
                          index: 0
                          delay: 10
                          value: 1
                      - bit:
                          index: 1
                          delay: 100
                          value: 1
                      - bit:
                          index: 2
                          delay: 10
                          value: 0
    
                    status_variables:
                      - variable:
                          addr: 100
                          delay: 100
                          value: 200
    
                  expected:
                    output_bits:
                      - bit:
                          index: 0
                          delay: 10
                          value: 1
                      - bit:
                          index: 1
                          delay: 100
                          value: 1
                      - bit:
                          index: 2
                          delay: 10
                          value: 0
    
                    da_output:
                      pressure: 10
                      flow: 20
                      back_pressure: 30
    
                    alarms:
                      - bit:
                          index: 0
                          delay: 50
                          value: 1
        """))

    print(action_tester)
    print(yaml.dump(action_tester.to_hash(),  
              default_flow_style=False))
