'''
Created on Aug 9, 2012

@author: gausscheng
'''

from random import randint
from ic_communicate.ic_transceiver_data import ICIMMTransceiverData
from ic_communicate.ic_serial_transceiver import ICSerialTransceiver

if __name__ == '__main__':
    serial_transceiver = ICSerialTransceiver('/dev/ttyS0')
    data_frame = ICIMMTransceiverData()
    sent_frame = ICIMMTransceiverData()
    sent_frame.function_code = 81
    sent_frame.addr = 2 << 8 | 208
    sent_frame.length = 27
    
    t = 0.0
    f = 0.0
    while True:
        serial_transceiver.write(sent_frame.data_frame_to_data_stream())
        recv = serial_transceiver.read(256)
        if len(recv) == 0:
            writed = sent_frame.data_frame_to_data_stream()
            for d in writed:
                print (d, end=' ')
            print ("End")
        if not data_frame.data_stream_to_data_frame(recv, len(recv), data_frame, sent_frame):
            f += 1
            for d in recv:
                print (d, end=' '),
            print ("End")
        else: t += 1
        print ("s radio:", t, f, t / (t + f))
        sent_frame.addr = randint(1, 700)
        sent_frame.function_code = 81
        sent_frame.length = randint(1, 16)
        sent_frame.data_buffer = []
        for i in range(0, sent_frame.length):
            sent_frame.data_buffer.append(randint(0, 65535))
        
    print ("End")