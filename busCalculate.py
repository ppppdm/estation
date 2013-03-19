# -*- coding: gbk -*-
'''
busCalculate.py ���㹫��������·�ϵ�λ��.

���ݸù���������·�͹�����������,ȷ������������·�ϵ�λ��

����:
    lineTable ---- ��·���б�
    lineDistTable ---- ��·�����б�,��lineDistance.py����
    busInfo ----��������Ϣ

����:
    lineBusTable----���������λ�ù�����λ�õ���·
    
busInfo ��������Ϣ:
    ��id,������·����,����,γ��
    
lineBusTable :
    lineBusTable�е���·��lineTable�е���·һһ��Ӧ,
    ����ÿ����·�ǰ������������·��λ�õĹ���������·

lineBusLine :
    ���������·��λ�õĹ���������·,��lineBusTable�е�һ��Ԫ��
    LineBusLine��һ��List,����elemOfLineBus
    �ṩ�Ĳ���:
    1.����վ������,���ص�һ�������վ�����վ��վ��
    2.����վ������,���ص�һ�������վ�����վ�ľ���
    3.����վ������,����ǰ���������վ�����վ��վ��
    4.����վ������,����ǰ���������վ�����վ��վ��
    
elemOfLineBus:
    elemOfLineBus ��������Ϣ
    1.վ������/id,��վ��վ������/idΪ'-1'
    2.��վ����һվ�ľ���
    3.��һվ����վ�Ĺ�����
    
    �ṩ�Ĳ���:
    1.���ݹ�������,����վ�����һ��������
    2.���ݹ�������,�Ӹ�վ��ɾ��һ��������
    
'''
import codecs
from busStopCalculate import updateLineStopBus
from lineDistance import lineDistTable
from lineDistance import linesTable

# Global variables for bus Calculte
LINE_STATION_COORDINATE = list()


# Must init below global variables when use this model


class busInfo:
    def __init__(self, id=None, lineName=None, lng=None, lat=None):
        self.id=id
        self.lineName=lineName
        self.lng=lng
        self.lat=lat
    
    def readDataPackage(self, dataPack):
        #����dataPackage �е����ݸ�ʽ��ȷ����ȡ�ķ���
        #����dataPack���Ѿ�ȥ�����ݰ�ͷβ������
        self.id=str(dataPack[0:4], 'gbk')
        self.lineName=[str(dataPack[4:8], 'gbk').strip(), str(dataPack[8:12], 'gbk')]
        self.lng=float(str(dataPack[12:20], 'gbk'))/600000
        self.lat=float(str(dataPack[20:28], 'gbk'))/600000
        return
    
    def getLineName(self):
        return self.lineName

class busInfo_cal():
    def __init__(self, id, line, station, dist):
        self.id=id
        self.line=line
        self.station=station #it could be the bias of the station in the line
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
    
    def toString(self):
        s=str(self.id)+'\t'+str(self.line)+'\t'+str(self.station)+'\t'+str(self.dist)
        return s

#���ڼ�¼��������Ϣ�ı�
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
        oldinfo=self.findById(info.id)
        if oldinfo:
            oldinfo.set(info)
        else:
            #��Ӳ���ע������
            self.table.append(info)
        return

    def write_to_file(self, filename):
        file=open(filename, 'w')
        s=''
        for info in self.table:
            s+=info.toString()+'\n'
        file.write(s)
        file.close()
        return
    
class elemOfLineBus:
    def __init__(self, name, dist):
        self.name=name ##station name
        self.dist=dist
        self.buses=[] ##list�д�ŵ���businfo��busId(or busindex in businfo)�����ǵ���վ�ľ���,��Ҫ�޸�!!!
        return
    
    def toString(self):
        return self.name+'\t'+str(self.dist)+str(self.buses)
'''
Ԫ����һ��line,ÿ��line�е�Ԫ����elemOfLineBus
'''
class lineBusTable:
    def __init__(self):
        self.table=[]
    '''
    argument:
    busId ----
    lineIndex ----
    station ----  bias of the station in this line
    '''
    def addbus(self, busId, lineIndex, station):
        line=self.table[lineIndex]
        line[station].buses.append(busId)
        return
    
    def delbus(self, busId, lineIndex, station):
        line=self.table[lineIndex]
        st=line[station]
        for bus in st.buses:
            if bus==busId:
                st.buses.remove(bus)
        return
    
    def read_from_dist_file(self, filename):
        file=open(filename, 'r')
        #��ȡ����linedist���ļ�,��ʽ:lng  lat dist    ��ʶ  ...
        while True:
            line=file.readline()
            line=line.rstrip('\n')
            if line=='':
                break
            else:
                arr=line.split('\t')
                self._insertDistLine(arr)
        file.close()
        return
    
    def read_from_file(self, filename):
        file=codecs.open(filename, 'r', 'gbk')
        #��ȡ����linedist���ļ�,��ʽ:lng  lat dist    ��ʶ  ...
        while True:
            line=file.readline()
            line=line.rstrip('\r\n')
            if line=='':
                break
            else:
                arr=line.split('\t')
                self._insertLine(arr)
        file.close()
        return
    
    def _insertDistLine(self, arr):
        line=[]
        for i in range(0, len(arr), 4):
            elem=elemOfLineBus(arr[i+3], float(arr[i+2]))
            line.append(elem)
        self.table.append(line)
        return
    
    def _insertLine(self, arr):
        line=[]
        for i in range(0, len(arr), 2):
            elem=elemOfLineBus(arr[i], float(arr[i+1]))
            line.append(elem)
        self.table.append(line)
        return
    
    def write_to_file(self, filename):
        file=open(filename, 'w')
        s=''
        for line in self.table:
            for elem in line:
                s+=elem.name+'\t'+str(elem.dist)+'\t'
            s=s.rstrip('\t')
            s+='\n'
        file.write(s)
        file.close()
        return
    
    def writeOneLine(self, filename, index):
        file=open(filename, 'w')
        s=''
        line=self.table[index]
        for elem in line:
            s+=elem.name+'\t'+str(elem.dist)+'\n'
        file.write(s)
        file.close()
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
���幫�����������߶�AB��ĩ��B��̾���bed
    1.����������C��ֱ��AB�Ĵ��߽��ڵ�D,��D���߶�AB��,��DB��Ϊ����
    2.ͬ1������,�����㲻���߶�AB��,��CB�ڹ���Ϊ����
    
distOfBusToSegmentEnd ��������һ��Ԫ��(bed,dist)
bed ---- �������������߶�AB��ĩ��B��̾���
dist ---- ���������߶�AB�ľ���,�����lineDistance.py

'''
def distOfBusToSegmentEnd(bus, pA, pB):
    #���ڼ���ĵ���붼�ܽ�,���Խ�3���㿴��һ��ƽ����
    bed, dist=0, 0
    a=lineDistance.distOfPointToPoint(pA, pB)
    b=lineDistance.distOfPointToPoint(bus, pB)
    c=lineDistance.distOfPointToPoint(pA, bus)
    #print(a, b, c)
    '''
    ���ǵ����㾫�ȵ�����,��a,b,c����һ��С��r(r�ӽ�0),�򲻼���x,AD,BD
    ���⵱x��ֵС��r(��bus�ӽ�AB���ڵ�ֱ��),���㿪��Ҳ�����ھ��ȵ�������
    ����r��ʱȡ0.0001
    '''
    r=0.0001
    #d=maxAngleCos(a, b, c)
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
    ##���ǽӽ�180�����ǵ�cosֵ�ӽ�-1
    elif maxAngleCos(a, b, c) - (-1)< r:
        #print(4, d+1)
        bed=b
        if a > b and a > c:
            dist=0
        else :
            dist=min(b, c)
    else :
        #�����C��ֱ��AB�ľ���
        ##x=��(2(a^2 b^2+a^2 c^2+b^2 c^2)-(a^4+b^4+c^4))/2a
        x=math.sqrt(2*(a**2*b**2 + a**2*c**2 + b**2*c**2) - (a**4 + b**4 + c**4)) / (2 * a)
        #print(5, x)
        #�жϹ���C���Ĵ�����ֱ��AB�Ľ���D�Ƿ����߶�AB��
        #�����߶�AD��BD�ĳ���,��AD > AB �� BD > AB,�򽻵�D�ڲ��߶�AB��
        ##AD^2+x^2=AC^2
        ##BD^2+x^2=BC^2
        AD=math.sqrt(c**2-x**2)
        BD=math.sqrt(b**2-x**2)
        if AD > a or BD > a:
            onAB=False
        else:
            onAB=True
    
        #����AD,BD��С�жϹ������������߶ε�ĩ�˾���
        if onAB:
            bed=BD
            dist=x
        else:
            bed=b
            dist=min((b, c))
    
    return bed, dist
'''
���㹫��������·����ʻ����һվ
����:
    lineDist ---- list of elemOfLineDist, elemOfLineDist��lineDistance.py
    busPoint ---- ��������γ��
����ֵ:
    position ---- (����������һվ����lineDist���±�,������һվ�ľ���)
'''

def calculateBusNextStation(lineDist, busPoint):
    minp2s=float('Infinity')
    bias=0
    dist=0
    for i in range(len(lineDist)-1):
        #print(i)
        pA=lineDist[i].getCoordinate()
        pB=lineDist[i+1].getCoordinate()
        
        #��������һ��Ԫ��(���������߶��յ�ľ���,�㵽�߶εľ���)
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
    #bias+1��������һվ
    return (bias+1, dist)


'''
���㹫��������·�ϵ�λ��
��ȡ��������������Ϣ(busInfo),��·�����������Ϣ(lineDistTable)
ͨ������,�ó���������һվ����һվ�;�����һվ�ľ���,
����������Ϣд��lineBusTable��
'''
def busPositionCalculate(lineDist, busInfo):
    #�����busInfo�е�bus����λ��
    busPoint=[busInfo.lng, busInfo.lat]
    position=calculateBusNextStation(lineDist, busPoint)
    return position

'''
����˵��:
1.position ---- �ڸ���·�ϵ�ƫ����,����һվ����
2.lineDist ---- ����·��վ�����
3.lineIndex ----����·����·���е�ƫ��
4.lineBusTable ---- ��·������,��Ҫ����lineIndex�ҵ����������ڵ���·
5.busInfoTable ---- ������Ϣ��,����������ԭ�����ڵ���·
'''
def updateTheLine(position, lineDist, lineIndex, lineBusTable, lineTable, busInfo, busInfoTable):
    #first update the lineBusTable,del old position,add new position
    busId=busInfo.id
    oldbus=busInfoTable.findById(busId)
    if oldbus != None:
        oldline=oldbus.getLine()
        oldstation=oldbus.getStation()
        oldlineIndex=lineTable.getIndexByFullName(oldline)
        lineBusTable.delbus(busId, oldlineIndex, oldstation)
    
    print(lineIndex)
    newline=lineTable.index(lineIndex)
    print(newline)
    newstation=position[0]#lineDist[position[0]].getStationId()# error ����·���е�ƫ������ȷ��վ,idΪ-1�����ظ�
    print(newstation)
    lineBusTable.addbus(busId, lineIndex, newstation)
    
    line=lineBusTable.table[lineIndex]
    for i in line:
        print(i.toString())
    
    #second update busInfoTable
    bus_cal=busInfo_cal(busId, newline, newstation, position[1])
    busInfoTable.update(bus_cal)
    
    #third get all station need update sending informateion
    updateLineStopBus(line, busInfoTable)
    return
'''
���ݹ�������Ϣ������·��������ͼ����Ĺ�������Ϣ��
��·���������а���������·
ÿ����·�ϰ���վ��(��lineDistTable��վ��һ��)
ÿ��վ���¼����һվ�ľ���͵���վ�Ĺ�����id�б�

�����Ĺ�������Ϣ�� busInfo_cal
�������й������ļ�¼
ÿ����¼������������·�ͽ�Ҫ����վ

�������������λ�ú����ԭ����¼�ڼ����Ĺ�������Ϣ���иó�����Ϣ
������·��������,
���Ƚϼ����Ĺ�������Ϣ����ԭ����λ��,ȷ����Щվ����Ҫ���·����µ���Ϣ
�����¼����Ĺ�������Ϣ
'''
def updateLineBus(lineTable, lineDistTable, lineBusTable, busInfoTable, busInfo):
    lineName=busInfo.getLineName()
    print('linename:', lineName)
    lineIndex=lineTable.getIndexByFullName(lineName)
    print('line index', lineIndex)
    lineDist=lineDistTable.index(lineIndex)
    #lineBus=lineBusTable(lineIndex)
    
    #��������һ��Ԫ��(����һվ��ƫ����,����һվ����)
    position=busPositionCalculate(lineDist, busInfo)
    print(position)
    #update line
    updateTheLine(position, lineDist, lineIndex, lineBusTable, lineTable, busInfo, busInfoTable)
    return

###############################################
class busCalculate:
    def __init__(self):
        self.linestable=None
        self.linedisttable=None
        self.linebustable=None
        self.businfotable=None
        
        self.linestable=linesTable()
        self.linestable.read_from_file('lines.txt')
        
        self.linedisttable=lineDistTable()
        self.linedisttable.read_from_file('linedist.txt')
        
        self.linebustable=lineBusTable()
        self.linebustable.read_from_file('linebus.txt')
        
        self.businfotable=busInfoTable()
        return
    
    def calculateBusPosition(self, businfo):
        print('This function no test')
        '''
        # get line name
        line_name = businfo.getLineName()
        # get line from linedistTable by line name
        bias = self.linestable.getIndexByFullName(line_name)
        line = self.linedisttable.index(bias)
        pos = busPositionCalculate(line, businfo)
        print(pos)
        '''
        # call updateLineBus
        updateLineBus(self.linestable, self.linedisttable, self.linebustable, self.businfotable, businfo)
        return

###############################################

if __name__=='__main__':
    from testBusFile import bus
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
    
    
    print('test busPositionCalculate')
    bi1=busInfo(7132, ['302', '����'], 118.216046, 33.95997)
    ret=busPositionCalculate(ldt.index(0), bi1)
    print(ret)
    
    
    print('test lineBusTable')
    #lineBusTable �Ĺ������lineDistTable��ͬ
    lbt=lineBusTable()
    lbt.read_from_dist_file('linedist.txt')
    lbt.write_to_file('linebus.txt')
    
    lbt2=lineBusTable()
    lbt2.read_from_file('linebus.txt')
    lbt2.write_to_file('tmp5.txt')
    lbt2.writeOneLine('tmp6.txt', 0)
    
    print('test busInfo_cal')
    bic=busInfo_cal(7132, ['302', '����'], 12, 0.0)
    s=bic.toString()
    print(s)
    
    
    print('test updateLineBus')
    lt=linesTable()
    lt.read_from_file('lines.txt')
    bit=busInfoTable()
    #updateLineBus(lineTable, lineDistTable, lineBusTable, busInfoTable, busInfo)
    updateLineBus(lt, ldt, lbt,bit,bi1)
    bit.write_to_file('tmp7.txt')
    #need to print bit
    
    
    bi2=busInfo(7132, ['302', '����'], 118.222567, 33.954176)
    updateLineBus(lt, ldt, lbt,bit,bi2)
    bit.write_to_file('tmp8.txt')
    print('exit')
