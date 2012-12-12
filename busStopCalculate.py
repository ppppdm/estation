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
        self.name=''
        self.buses=[None]*2 #buses中元素仅记录bus到站的距离
        return
    
    def setName(self, name):
        self.name=name
    
    def getName(self, name):
        return self.name
    
    def setBus(self, buses):
        self.buses=buses
    
    def getBus(self):
        return self.buses

class busQueue:
    def __init__(self, len):
        self.queue=[None]*len
        self.bias=0
        self.len=len
    
    def insert(self, bus):
        self.queue[self.bias]=bus
        self.bias+=1
        if self.bias >= self.len:
            self.bias=0

    
    #N 代表第几个,第一个从1开始
    def getNth(self, n):
        return self.queue[(self.bias-n)%self.len]
    
    def setNth(self, n, v):
        self.queue[(self.bias-n)%self.len]=v



####################################################
def getBusDist(buses, bustable):
    dist =[]
    for i in buses:
        info=bustable.findById(i)
        dist.append(info.dist)
    return dist

def addBuses(buses, bq):
    #首先对buses进行排序,距离大的排在前面
    buses.sort(reverse=True)
    print(buses)
    #将buses加入到bq中
    for bus in buses:
        bq.insert(bus)
    return
'''
updateLineStopBus 根据之前的lineBus计算结果获取线路上每个公交站的到其的
前两辆公交车距离该站的距离
从线路的起始站开始,找到两辆公交车,并计算这两辆公交车到该站的距离.
若已经有两辆公交车,又找到了一辆新的公交车,则新公交车为首辆到达的公交车
原来首辆到达的公交车变为次到达此战的公交车.

对于站点标识为'-1'的不将其加入到linestopbus中
'''
def updateLineStopBus(lineBus, bustable):
    mlineStopBus=[]
    bq=busQueue(2)
    
    for stop in lineBus:
        print(stop)
        #buses中是id,通过id在bustable中找到该bus距离!!!!
        #简化,buses中存有距离
        busdist=getBusDist(stop.buses, bustable)
        addBuses(busdist, bq)
        
        if stop.name != '-1':
            sbus=stopBus()
            sbus.setName(stop.name)
            bus=[bq.getNth(1), bq.getNth(2)]
            sbus.setBus(bus)
            mlineStopBus.append(sbus)

        for v in bq.queue:
            v+=stop.dist
    return mlineStopBus

if __name__=='__main__':
    print('test')
    print('test busQueue')
    bq=busQueue(2)
    bq.insert(3)
    print(bq.getNth(1))
    bq.insert(4)
    print(bq.getNth(1))
    bq.setNth(1, 9)
    print(bq.getNth(1))
    bq.insert(0)
    print(bq.getNth(1))
    
    print('test addBuses')
    addBuses([2, 5, 7], bq)
    print(bq.getNth(1))
    print(bq.getNth(2))
    
    
    print('test updateLineStopBus')
    #lsb = updateLineStopBus()
    
    print('exit')
