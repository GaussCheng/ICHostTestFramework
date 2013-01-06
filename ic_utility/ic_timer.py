'''
Created on Aug 14, 2012

@author: gausscheng
'''
from datetime import datetime


class ICTimer(object):
    '''
    timer class
    '''
    
    ICTIMER_STOP_STATUS     = 0
    ICTIMER_RUNNING_STATUS  = 1
    
    def __init__(self):
        self._started_time_ = 0
        self._timer_status_ = self.ICTIMER_STOP_STATUS
    
    def start(self):
        self._timer_status_ = self.ICTIMER_RUNNING_STATUS
        self._started_time_ = datetime.now()
    
    def restart(self):
        if self._timer_status_ == self.ICTIMER_RUNNING_STATUS:
            now = datetime.now()
            ret = (now - self._started_time_).microsecond
            self._started_time_ = now
            return ret
        self.start()
        return 0        
    
    def elapsed(self):
        if self._timer_status_ == self.ICTIMER_RUNNING_STATUS:
            return (datetime.now() - self._started_time_).microsecond
        return 0