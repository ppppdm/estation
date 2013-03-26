# -*- coding: gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
#
# stationBusInfo.py define the station in one Line's bus arrive infomation
# sturct{
#    name
#    line
#    line_dir
#    s_bus []
#        }
# In the struct (name,line,line_dir) unique identify a station. The (s_bus)
# is a struct that store the buses information arrive this station.
# struct s_bus{
#     station_count
#     distance
#     bus_status
#             }

class busDis:
    def __init__(self, station_count=None, distance=None, bus_stauts=None):
        self.station_count = station_count
        self.distance = distance
        self.bus_stauts = bus_stauts

class stationArriveInfo:
    def __init__(self, name, line, line_dir, s_bus):
        self.name = name
        self.line = line
        self.line_dir = line_dir
        self.s_bus = s_bus
    
    def toString(self):
        return str(self.name)+', '+str(self.line)+', '+str(self.line_dir)+', '+str(self.s_bus)

# This function setOneLineStationArriveInfo() use busLine info and the bus 
# position info to set the stations in this line bus arrive info.
# The realBusPos should be sorted increas before.
def setOneLineStationArriveInfo(lineName, lineDirt, lineStations, realBusPos):
    stations = []
    i, j=0, 0
    # for not over index of realBusPos append a infinity to realBusPos
    # (alse a munber bigger than the len of lineStations
    realBusPos.append(len(lineStations))
    
    for st in lineStations:
        if realBusPos[j] <= i:
            j+=1
        # now I use calculate at once
        # if have distance may use Accumulate
        buses = [arriveStCount(realBusPos, j, i, 1), arriveStCount(realBusPos, j, i, 2)]
        stai = stationArriveInfo(st[0], lineName, lineDirt, buses)
        stations.append(stai)
        i+=1
    return stations

# bp_bias means the bias in realBusPosition
# st_bias means the station bias in the line
# nth should bigger than 0, like 1,2,...
def arriveStCount(realBusPos, bp_bias, st_bias, nth):
    if nth <= 0:
        return None
    index = bp_bias - nth
    if index < 0:
        return None
    
    return st_bias - realBusPos[index]


if __name__=='__main__':
    print(__file__, 'test!')
    import os
    import sys
    parent_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(parent_path)
    
    from lineDistance import lineStopTable
    from lineDistance import linesTable
    lt = linesTable()
    lt.read_from_file('..\lines.txt')
    
    lst=lineStopTable()
    lst.read_from_file('..\linestop.txt')
    
    line_stations = lst.index(0)
    line = lt.index(0)
    print(line)
    
    #print(line_stations)
    sac = setOneLineStationArriveInfo(line[0], line[1], line_stations, [4, 20, 28])
    for i in sac:
        print(i.toString())
    
    
    
    
    
    
