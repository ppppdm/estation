# -*- coding: gbk -*-
# auther : pdm
# email : ppppdm@gmail
#
# Transform bus Position from virtual to real

import os
import sys
parent_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_path)

# Transform one bus postion from virtual to real
# @ primary
# @ args
#       vPos : virtual position of one bus
#       line : the line that the bus drived on, line consist of all stations
#              that we can now wether it's a virtual or real station
# @ return
#       rPos : real position of one bus
def virtual_2_real(vPos, line):
    for st in line[vPos:]:
        if st.isRealStation():
            rPos = st.realPos
            break
    return rPos

# Using for transform one line vitrual postions
def oneLineBusesVirtual2Real(vPosList, line):
    realBusesPostion = []
    for vPos in vPosList:
        rPos = virtual_2_real(vPos, line)
        realBusesPostion.append(rPos)
    return realBusesPostion


if __name__=='__main__':
    print(__file__, 'test')
    import lineDistance
    ldt = lineDistance.lineDistTable()
    ldt.read_from_file('..\linedist.txt')
    
    # test virtual2real
    vPos = 10
    line = ldt.index(0)
    print(virtual_2_real(10, line))
    
    print(oneLineBusesVirtual2Real([10,16], line))
    
