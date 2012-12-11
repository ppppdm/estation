# -*- coding: gbk -*-
'''
busCalculate.py 计算公交车在线路上的位置.

根据该公交所属线路和公交车的坐标,确定公交车在线路上的位置

参数:
    lineTable ---- 线路的列表
    lineDistTable ---- 线路距离列表,由lineDistance.py计算
    busInfo ----公交车信息

返回:
    lineBusTable----包含计算好位置公交车位置的线路
    
busInfo 包含的信息:
    车id,所属线路名字,经度,纬度
    
lineBusTable :
    lineBusTable中的线路与lineTable中的线路一一对应,
    其中每条线路是包含计算好在线路中位置的公交车的线路

lineBusLine :
    计算好在线路中位置的公交车的线路,是lineBusTable中的一个元素
    LineBusLine是一个List,包含elemOfLineBus
    提供的操作:
    1.根据站的名字,返回第一辆到达该站车距该站的站数
    2.根据站的名字,返回第一辆到达该站车距该站的距离
    3.根据站的名字,返回前两辆到达该站车距该站的站数
    4.根据站的名字,返回前两辆到达该站车距该站的站数
    
elemOfLineBus:
    elemOfLineBus 包含的信息
    1.站点名字/id,非站点站的名字/id为'-1'
    2.该站距下一站的距离
    3.下一站到该站的公交车
    
    提供的操作:
    1.根据公交车号,给该站点添加一辆公交车
    2.根据公交车号,从该站点删除一辆公交车
    
'''

class busInfo:
    def __init__(self, id, lineName, lng, lat):
        self.id=id
        self.lineName=lineName
        self.lng=lng
        self.lat=lat
    
    def readDataPackage(self, dataPack):
        #根据dataPackage 中的数据格式来确定读取的方法
        return
    
    def getLineName(self):
        return self.lineName

class busInfo_cal():
    def __init__(self, id, line, station, dist):
        self.id=id
        self.line=line
        self.station=station
        self.dist=dist
    
    def getLine(self):
        return self.line
    
    def getStation(self):
        return self.station
    
    def getDist(self):
        return self.dist
    
    def setLine(self, line):
        self.line=line
    
    def setStation(self, station):
        self.station=station
    
    def set(self, info):
        self.line=info.line
        self.station=info.station
        self.dist=info.dist

#用于记录公交车信息的表
class busInfoTable():
    def __init__(self):
        self.table=list()
    
    def findById(self, id):
        for info in self.table:
            if info.id == id:
                return info
        return None
    
    #add a businfo to table if the id of businfo not in table,
    #if not update the businfo status
    def update(self, info):
        oldinfo=self.findById(info)
        if oldinfo:
            oldinfo.set(info)
        else:
            #添加操作注意上锁
            self.table.append(info)
        return

class elemOfLineBus:
    def __init__(self, name, dist):
        self.name=name
        self.dist=dist
        self.buses=[] ##list中存放的是businfo的busId(or busindex in businfo)
        return
'''
元素是一条line,每条line中的元素是elemOfLineBus
'''
class lineBusTable:
    def __init__(self):
        self.table=[]
    
    def addbus(self, busId, lineIndex, station):
        line=self.table[lineIndex]
        for st in line:
            if st.name==station:
                st.buses.append(busId)
                break
        return
    
    def delbus(self, busId, lineIndex, station):
        line=self.table[lineIndex]
        for st in line:
            if st.name==station:
                for bus in st.buses:
                    if bus==busId:
                        st.buses.remove(bus)
        return

###############################################
import lineDistance
import math


def maxAngleCos(a, b, c):
    sides=[a, b, c]
    maxs=max(sides)
    sides.remove(max(sides))
    e, f=0, 2
    for i in sides:
        e+=i**2
        f*=i
    C=(e-maxs**2)/f
    return C

'''
定义公交车到有向线段AB的末端B最短距离bed
    1.若过公交车C做直线AB的垂线交于点D,若D在线段AB上,则DB即为所求
    2.同1的做法,若交点不在线段AB上,则CB在公交为所求
    
distOfBusToSegmentEnd 函数返回一个元组(bed,dist)
bed ---- 公交车到有向线段AB的末端B最短距离
dist ---- 公交车到线段AB的距离,定义见lineDistance.py

'''
def distOfBusToSegmentEnd(bus, pA, pB):
    #由于计算的点距离都很近,所以将3个点看成一个平面上
    bed, dist=0, 0
    a=lineDistance.distOfPointToPoint(pA, pB)
    b=lineDistance.distOfPointToPoint(bus, pB)
    c=lineDistance.distOfPointToPoint(pA, bus)
    #print(a, b, c)
    '''
    考虑到计算精度的问题,当a,b,c任意一个小于r(r接近0),则不计算x,AD,BD
    另外当x的值小于r(即bus接近AB所在的直线),计算开方也将由于精度导致问题
    这里r暂时取0.0001
    '''
    r=0.0001
    d=maxAngleCos(a, b, c)
    #print(a, b, c, d+1)
    if a < r:
        #print(1, a)
        bed=a
        dist=b
    elif b < r:
        #print(2, b)
        bed=b
        dist=b
    elif c < r:
        #print(3, c)
        bed=a
        dist=c
    ##最大角接近180即最大角的cos值接近-1
    elif d - (-1)< r:
        #print(4, d+1)
        bed=b
        if a > b and a > c:
            dist=0
        else :
            dist=min(b, c)
    else :
        #计算点C到直线AB的距离
        ##x=√(2(a^2 b^2+a^2 c^2+b^2 c^2)-(a^4+b^4+c^4))/2a
        x=math.sqrt(2*(a**2*b**2 + a**2*c**2 + b**2*c**2) - (a**4 + b**4 + c**4)) / (2 * a)
        #print(5, x)
        #判断过点C作的垂线与直线AB的交点D是否在线段AB上
        #计算线段AD和BD的长度,若AD > AB 或 BD > AB,则交点D在不线段AB上
        ##AD^2+x^2=AC^2
        ##BD^2+x^2=BC^2
        AD=math.sqrt(c**2-x**2)
        BD=math.sqrt(b**2-x**2)
        if AD > a or BD > a:
            onAB=False
        else:
            onAB=True
    
        #根据AD,BD大小判断公交车到有向线段的末端距离
        if onAB:
            bed=BD
            dist=x
        else:
            bed=b
            dist=min((b, c))
    
    return bed, dist
'''
计算公交车在线路上行驶的下一站
参数:
    lineDist ---- list of elemOfLineDist, elemOfLineDist见lineDistance.py
    busPoint ---- 公交车经纬度
返回值:
    position ---- (公交车到下一站的在lineDist的下标,距离下一站的距离)
'''

def calculateBusNextStation(lineDist, busPoint):
    minp2s=float('Infinity')
    bias=0
    dist=0
    for i in range(len(lineDist)-1):
        #print(i)
        pA=lineDist[i].getCoordinate()
        pB=lineDist[i+1].getCoordinate()
        
        #函数返回一个元组(公交车到线段终点的距离,点到线段的距离)
        ret=distOfBusToSegmentEnd(busPoint, pA, pB)
        p2s=ret[1]
        #print(ret, bias)
        #compare method of judge weather the bus in this segment,two way
        #1.the minimun dist
        #2.when the dist less than 
        if p2s < minp2s:
            minp2s=p2s
            bias=i
            dist=ret[0]
    #bias+1表明到下一站
    return (bias+1, dist)


'''
计算公交车在线路上的位置
获取公交车的坐标信息(busInfo),线路点坐标距离信息(lineDistTable)
通过计算,得出公交车下一站到哪一站和距离那一站的距离,
将计算后的信息写入lineBusTable中
'''
def busPositionCalculate(lineDist, busInfo):
    #计算出busInfo中的bus的新位置
    busPoint=[busInfo.lng, busInfo.lat]
    position=calculateBusNextStation(lineDist, busPoint)
    return position

'''
参数说明:
1.position ---- 在该线路上的偏移量,到下一站距离
2.lineDist ---- 该线路的站点距离
3.lineIndex ----该线路在线路表中的偏移
4.lineBusTable ---- 线路公交表,需要根据lineIndex找到车现在所在的线路
5.busInfoTable ---- 公交信息表,包含公交车原来所在的线路
'''
def updateTheLine(position, lineDist, lineIndex, lineBusTable, lineTable, busInfo, busInfoTable):
    #first update the lineBusTable,del old position,add new position
    busId=busInfo.id
    oldbus=busInfoTable.findById(busId)
    oldline=oldbus.getLine()
    oldstation=oldbus.getStation()
    oldlineIndex=lineTable.getIndexByName(oldline)
    
    newline=lineDistTable.index(lineIndex)
    newstation=newline[position[0]].getStationId()

    lineBusTable.delbus(busId, oldlineIndex, oldstation)
    lineBusTable.addbus(busId, lineIndex, newstation)
    
    #second get all station need update sending informateion and add to stationInfo
    ##call stationInfo func
    
    
    #third update busInfoTable
    bus_cal=busInfo_cal(busId, newline, newstation, position[1])
    busInfoTable.update(bus_cal)
    return
'''
根据公交车信息更新线路公交车表和计算后的公交车信息表
线路公交车表中包含所有线路
每条线路上包含站点(与lineDistTable的站点一样)
每个站点记录到下一站的距离和到该站的公交车id列表

计算后的公交车信息表 busInfo_cal
包含所有公交车的记录
每条记录公交车所在线路和将要到的站

计算出公交车的位置后根据原来记录在计算后的公交车信息表中该车的信息
更新线路公交车表,
并比较计算后的公交车信息表中原来的位置,确定哪些站点需要重新发布新的信息
最后更新计算后的公交车信息
'''
def updateLineBus(lineTable, lineDistTable, lineBusTable, busInfoTable, busInfo):
    lineName=busInfo.getLineName()
    lineIndex=lineTable.getIndexByName(lineName)
    lineDist=lineDistTable.index(lineIndex)
    #lineBus=lineBusTable(lineIndex)
    
    #函数返回一个元组(到下一站的偏移量,到下一站距离)
    position=busPositionCalculate(lineDist, busInfo)
    
    #update line
    updateTheLine(position, lineDist, lineIndex, lineBusTable, lineTable, busInfo, busInfoTable)
    return

###############################################



if __name__=='__main__':
    from testBusFile import bus
    from lineDistance import lineDistTable
    print('test')
    bus1=bus()
    bus1.readFromFile('busone.txt')
    bus1.writeTofile('tmp3.txt')
    
    print("test distOfBusToSegmentEnd")
    ret=distOfBusToSegmentEnd((118.216117,33.963728), (118.214824,33.960854), (118.214824,33.960854))
    print(ret)
    
    
    print('test func calculateBusNextStation()')
    bus2=bus()
    bus2.readFromFile('bus2.txt')
    ldt=lineDistTable()
    ldt.read_from_file('linedist.txt')
    line=ldt.index(0)
    for i in bus1.path:
        pos=calculateBusNextStation(line, i)
        print(pos)
    
    print('exit')
