# -*- coding: gbk -*-
# auther : ppppdm
# email  : ppppdm@gmail.com
#
# stationInfoManager.py
#   The stationInfoManager each time get one line bus positions from busPositioinDT.
# Then transform bus position virtual to real. At last calculate station bus info by
# bus real position.
#   The Line get from table of line. Here every 0 seconds to get one line from busPo-
# sitioinDT.

import threading
import time
import globalValues
import sys
from ds import busPosition_V2R
from ds import stationBusInfo



def round_add(i, max):
    i += 1
    if i >= max:
        i = 0
    return i

class stationInfoManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        i = 0
        lineNum  = globalValues.lines.getNum()
        try:
            while True:
                lineName = globalValues.lines.index(i)
                line = globalValues.linedist.index(i)
                stations = globalValues.linestop.index(i)
                i = round_add(i, lineNum)
                
                # get buses from busPositioinDT with line name
                buses = globalValues.bus_pos_dt.getOneLineBusPos(lineName)
                
                # transform bus position virtual to real
                realPos = busPosition_V2R.oneLineBusesVirtual2Real(buses, line)
                
                # calculate station bus info by bus real position
                sbi = stationBusInfo.setOneLineStationArriveInfo(lineName, stations, realPos)
                for st in sbi:
                    #print(st)
                    print(st.toString())
                # 
                
                time.sleep(1)
        except:
            tb = sys.exc_info()
            print('line :', tb[2].tb_lineno, tb[1])

        return
    
    

if __name__=='__main__':
    print(__file__, 'test')
    print(__name__)
    # test: insert data to globalValues.bus_pos_dt
    
    t = stationInfoManager()
    t.start()
