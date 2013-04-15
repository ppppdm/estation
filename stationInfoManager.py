# -*- coding: gbk -*-
# auther : ppppdm
# email  : ppppdm@gmail.com
#
# stationInfoManager.py
#   The stationInfoManager each time get one line bus positions from busPositioinDT.
# Then transform bus position virtual to real. At last calculate station bus info by
# bus real position.
#   The Line get from table of line. Here every 2 seconds to get one line from busPo-
# sitioinDT.

import threading

class stationInfoManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        return
    
    

if __name__=='__main__':
    print(__file__, 'test')
    print(__name__)
