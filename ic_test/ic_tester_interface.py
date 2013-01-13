'''
Created on Aug 11, 2012

@author: gausscheng
'''


def get_value_from_hash_helper(key, value_hash, default_value):
    if key in value_hash:
        return value_hash[key]
    return default_value


class YamlType(object):

    def to_hash(self):
        return {}

    def get_value_from_hash(self, value_hash):
        pass


class ICTesterInterface(YamlType):
    '''
    test case interface
    '''

#    g_serial_transceiver = ICSerialTransceiver("/dev/ttyS0")

    def __init__(self):
        '''
        Constructor
        '''
        pass

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
