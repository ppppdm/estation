# -*- coding: gbk -*-
# auther : pdm
# email : ppppdm@gmail
#
# Change the bus position in virtual line to real line.
# First get the line all bus position and the line virtual situation.
# Second For every bus in the line change its position to real position.
# The change algorithms :
#      bus
#       ↓
#     R v v R v v v R ....
# --> line dirct
#  1. find whether the bus next station is a real station. If it's the
# bus position is the staation real index from line head(start). If not,
# go to next step.
#  2. down with the line dirct get the first real station. So the station
# real index is the bus position.
#
#　 algorithms changed :
#   Down from the bus position with line direct get the first real station.
# The station's real index is the bus position.
import os
import sys
parent_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_path)

LINE_FILE = '..\linedist.txt'


def oneLineBusesVirtul2Real(lineBuses, line):
    realBusesPostion = []
    for bus in lineBuses:
        rPos = virtual2real(bus.vPos, line)
        realBusesPostion.append(rPos)
    return realBusesPostion

def virtual2real(vPos, line):
    for st in line[vPos:]:
        if st.isRealStation():
            rPos = st.realPos
            break
    return rPos

if __name__=='__main__':
    print(__file__, 'test')
    import lineDistance
    ldt = lineDistance.lineDistTable()
    ldt.read_from_file(LINE_FILE)
    
    
    #real_bus_pos = []
    #real_bus_pos = oneLineBusesVirtul2Real()
    
    
    
    
    
