'''
Created on Aug 9, 2012

@author: gausscheng
'''
from ic_utility.ic_crc16 import check_crc16, crc16

class ICTransceiverData(object):
    '''
    Communicate Frame 
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def is_query(self):
        return False
    
    def is_error(self):
        return False
    
    def is_equal(self, other):
        return False
    
    def max_frame_length(self):
        return 0
    

class ICIMMTransceiverData(ICTransceiverData):
    '''
    IMM Communicate Frame
    '''
    FUNCTION_CODE_BEGIN_SECTION = 0x49
    FUNCTION_CODE_READ = 0x50
    FUNCTION_CODE_WRITE = 0x51
    FUNCTION_CODE_ERR = 0x60
    FUNCTION_CODE_NIL = 0x61
    FRAME_HEAD_SIZE = 4
    FRAME_LENGTH_POS = FRAME_HEAD_SIZE - 1
    FRAME_DATA_LENGTH = 64
    FRAME_CRC_LENGTH = 2
    FRAME_MAX_SIZE = FRAME_HEAD_SIZE + (FRAME_DATA_LENGTH << 2) + 2
    FRAME_MIN_SIZE = FRAME_HEAD_SIZE + FRAME_CRC_LENGTH

    def __init__(self):
        self.function_code = self.FUNCTION_CODE_NIL
        self.addr = 0
        self.length = 0
        self.data_buffer = []
        
    def is_query(self):
        return self.function_code == self.FUNCTION_CODE_READ
        
    def is_error(self):
        return self.function_code == self.FUNCTION_CODE_ERR
    
    def is_equal(self, other):
        if isinstance(other, ICIMMTransceiverData):
            return (other.function_code == self.function_code and \
                    other.addr == self.addr and \
                    other.length == self.length and\
                    other.data_buffer == self.data_buffer)
    
    def max_frame_length(self):
        return self.FRAME_MAX_SIZE
    
    def is_function_code_vailid(self, fc):
        return (fc == self.FUNCTION_CODE_READ or  \
                fc == self.FUNCTION_CODE_WRITE or \
                fc == self.FUNCTION_CODE_ERR)
    
    def is_function_addr_valid(self, addr, fc):
        if fc == self.FUNCTION_CODE_READ:
            return addr > 0 and addr < 774
        elif fc == self.FUNCTION_CODE_WRITE:
            return addr > 0 and addr < 774
        elif fc == self.FUNCTION_CODE_ERR:
            return addr == 775
        else: return False
    
    def get_addr_from_buffer(self, data_stream):
        return ((ord(data_stream[1]) << 8) | ord(data_stream[2]))
    
    def get_data_stream_data_length(self, data_stream):
        return ord(data_stream[self.FRAME_LENGTH_POS]) << 2
    
    def data_stream_to_data_frame(self, data_stream, size, dest_frame, sent_frame):
        if not isinstance(dest_frame, ICIMMTransceiverData):
            return False
        if size < self.FRAME_MIN_SIZE:
            return False
        if not self.is_function_code_vailid(ord(data_stream[0])):
            return False
        temp_addr = self.get_addr_from_buffer(data_stream)
        if not self.is_function_addr_valid(temp_addr, ord(data_stream[0])):
            return False
        tmp_length = self.get_data_stream_data_length(data_stream)
        if tmp_length < self.FRAME_MIN_SIZE:
            return False
        if size != self.FRAME_MIN_SIZE + tmp_length:
            return False
        if not check_crc16(data_stream, size):
            return False
        
        dest_frame.function_code = ord(data_stream[0])
        dest_frame.addr = temp_addr
        data_length = tmp_length >> 2
        j = 4
        dest_frame.data_buffer = []
        i = 0
        while i < data_length: 
            dest_frame.data_buffer.append(ord(data_stream[j]) << 24 | \
                                         ord(data_stream[j + 1]) << 16 | \
                                         ord(data_stream[j + 2]) << 8 | \
                                         ord(data_stream[j + 3]))
            j += 4
            i += 1
        dest_frame.length = data_length
    
        if not dest_frame.is_query():
            if not dest_frame.is_equal(sent_frame):
                return False
        return True;
        
    def data_frame_to_data_stream(self):
        ret = bytearray()
        ret.append(self.function_code)
        ret.append(self.addr >> 8)
        ret.append(self.addr & 0x00FF)
        ret.append(self.length)
        for data in self.data_buffer:
            ret.append(data >> 24)
            ret.append(data >> 16)
            ret.append(data >> 8)
            ret.append(data & 0x00FF)
        crc = crc16(bytes(ret), len(ret))
        ret.append(crc >> 8)
        ret.append(crc & 0x00FF)
        return ret
    
    
