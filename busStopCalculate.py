#  -*- conding: gbk -*-
'''
根据线路上公交车情况,更新该线路公交站的信息
'''
class bus:
    def __init__(self, bias, dist):
        self.bias=bias
        self.dist=dist
        return
    
    def getBias(self):
        return self.bias
    
    def getDist(self):
        return self.dist

class stopBus:
    def __init__(self):
        self.buses=[None]*2 #buses中元素仅记录bus到站的距离
        return
    
    def setBus(self, buses):
        self.buses=buses
    
    def getBus(self):
        return self.buses

def addBuses(buses, bus2V):
    #首先对buses进行排序
    
    #bus2V中两辆车,第一辆当前最早的一辆,第二辆是次早的一辆
    return

def updateLineStopBus(lineBus):
    mlineStopBus=[]
    bus2V=[None]*2
    
    for stop in lineBus:
        print(stop)
        stop.name
        stop.dist
        addBuses(stop.buses, bus2V)
        if stop.name != '-1':
            print(1)
        else:
            print(2)
        print(bus2V)
    
    return mlineStopBus

if __name__=='__main__':
    print('test')
    
    print('exit')
