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
        self.buses=[] #buses中元素仅记录bus到站的距离
        return
    
    def setName(self, name):
        self.name=name
    
    def getName(self, name):
        return self.name
    
    def setBus(self, buses):
        self.buses=buses
    
    def getBus(self):
        return self.buses
    
    def toString(self):
        s=self.name+'\t'
        for bus in self.buses:
            s+=str(bus)+'\t'
        return s

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
    
    def getLen(self):
        return self.len


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
    #print(buses)
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
        #print(stop)
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

        for i in range(bq.getLen()):
            dist=bq.getNth(i)
            if dist !=None:
                bq.setNth(i, dist+stop.dist)
    
    file=open('tmp9.txt', 'w')
    s=''
    for i in mlineStopBus:
        s+=i.toString()+'\n'
    file.write(s)
    file.close()
    #for i in mlineStopBus:
    #    print(i.toString())
    return mlineStopBus

if __name__=='__main__':
    from lineDistance import linesTable
    from lineDistance import lineDistTable
    from busCalculate import busInfoTable
    from busCalculate import lineBusTable
    from busCalculate import busInfo
    import busCalculate
    import stopTable
    from stopTable import readBusStopTable
    from stopTable import BUSSTOPLIST
    
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
    bit=busInfoTable()
    lt=linesTable()
    lt.read_from_file('lines.txt')
    
    ldt=lineDistTable()
    ldt.read_from_file('linedist.txt')
    
    lbt=lineBusTable()
    lbt.read_from_dist_file('linedist.txt')
    
    bi2=busInfo(7132, ['302', '下行'], 118.222567, 33.954176)
    bi3=busInfo(7133, ['302', '下行'], 118.292437, 33.95726)
    
    busCalculate.updateLineBus(lt, ldt, lbt,bit,bi2)
    busCalculate.updateLineBus(lt, ldt, lbt,bit,bi3)
    
    for i in lbt.table[0]:
        print(i.buses)
    
    linebus=lbt.table[0]
    lsb = updateLineStopBus(linebus, bit)
    
    for i in lsb:
        print(i.toString())
    
    readBusStopTable('stopTable.txt', BUSSTOPLIST)
    
    for i in lsb:
        print(i.toString()) 
        print(stopTable.getSerialNumber(i.name,'302','下行'))
    
    print('exit')
