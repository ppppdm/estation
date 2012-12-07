'''
lineDistence.py 读入线路文件(lines.txt linestop.txt linepath.txt)生成线路间的距离(linedist.txt)
linedist.txt 格式如下:
    1.每行表示一条线路,对应lines.txt
    2.一行中列出地理坐标点(由经纬度表示)和距离下一个的距离
        lng1 lat1 dist1 站标识 lng2 lat2 dist2 站标识 [ ... ]
        (lng -- 经度, lat -- 维度, dist -- 距离,站标识 -- 站名或站编号,非站的用-1标识,这些数据以'\t'分隔)

lines.txt 格式如下:
    1.每行是一条线路,有线路名,上/下行
        name up/down

linestop.txt 格式如下:
    1.每行是一条线路,内容是从起点到终点的站和站的坐标
        stop1 lng1 lat1 stop2 lng2 lat2 [ ... ]

linepath.txt 格式如下:
    1.每行是一条线路,内容是线路坐标点
    lng1 lat1 lng2 lat2 [ ... ]
    
'''


class fileTable:
    def __init__(self):
        self.table=[]
    
    def read_from_file(self, filename):
        file=open(filename, 'r')
        while True:
            s=file.readline()
            if s=='':
                break
            else:
                s=s.rstrip('\n')
                arr=s.split('\t')
                self.insertLine(arr)
        file.close()
        return
        
    def write_to_file(self, filename, flags):
        file=open(filename, flags)
        for i in self.table:
            self.writeLine(file, i)
        file.close()
        return
    
    def getNum(self):
        return len(self.table)
        
    def index(self, i):
        return self.table[i]
    
    def insertLine(self, arr):
        self.table.append(arr)
    
    def writeLine(self, file, arr):
        s=''
        for i in arr:
            #print(i)
            s+=i+'\t'
        s=s.rstrip('\t')
        s+='\n'
        file.write(s)

#格式: name up/down
class linesTable(fileTable):
    def getLineName(self, i):
        line=self.index(i)
        if line:
            return line[0]
        return None
    
    def getLineUpOrLow(self, i):
        line=self.index(i)
        if line:
            return line[1]
        return None

#格式: stop1 lng1 lat1 stop2 lng2 lat2 [ ... ]
class lineStopTable(fileTable):
    def getOneLineNum(self,  i):
        line=self.index(i)
        if line:
            return len(line)
        return None

    def insertLine(self,  arr):
        line=[]
        for i in range(0, len(arr), 3):
            elem=[arr[i], arr[i+1], arr[i+2]]
            line.append(elem)
        self.table.append(line)
        return
    
    def writeLine(self, file, arr):
        s=''
        for elem in arr:
            for j in elem:
                s+=j+'\t'
        s=s.rstrip('\t')
        s+='\n'
        file.write(s)
        return
    
    def getOneStop(self, line, j):
        return line[j]

#格式:lng1 lat1 lng2 lat2 [ ... ]：
class linePathTable(fileTable):    
    def insertLine(self, arr):
        line=[]
        for i in range(0, len(arr), 2):
            elem=[arr[i], arr[i+1]]
            line.append(elem)
        self.table.append(line)
        return
    
    def writeLine(self, file, arr):
        s=''
        for elem in arr:
            for j in elem:
                s+=j+'\t'
        s=s.rstrip('\t')
        s+='\n'
        file.write(s)
        return


NOT_STATION='-1'

class elemOfLineDist:
    def __init__(self, lng, lat, dist=0, stationId=NOT_STATION):
        self.lng=lng
        self.lat=lat
        self.dist=dist
        self.isStaion=stationId
        return
    
    def getLng(self):
        return self.lng
    
    def getLat(self):
        return self.lat
    
    def getDist(self):
        return self.dist
    
    def getStationId(self):
        return self.isStaion
    
    def getCoordinate(self):
        return (self.lng, self.lat)
    
    def setDist(self, dist):
        self.dist=dist
    
#lng1 lat1 dist1 站标识 lng2 lat2 dist2 站标识 [ ... ]
class lineDistTable(fileTable):
    def insertLineWithArr(self, arr):
        line=[]
        for i in range(0, len(arr), 4):
            elem=elemOfLineDist(arr[i], arr[i+1], int(arr[i+2]), arr[i+3])
            line.append(elem)
        self.table.append(line)
        return
    
    def insertLine(self, line):
        self.table.append(line)
        return
    
    def writeLine(self, file, arr):
        s=''
        for elem in arr:
            s+=elem.getLng()+'\t'+elem.getLat()+'\t'+str(elem.getDist())+'\t'+elem.getStationId()+'\t'
        s.rstrip('\t')
        s+='\n'
        file.write(s)
        return
    
    def writeOneLine(self, filename, i):
        file=open(filename, 'w')
        line=self.index(i)
        s=''
        for elem in line:
            s+=elem.getLng()+'\t'+elem.getLat()+'\t'+str(elem.getDist())+'\t'+elem.getStationId()+'\n'
        
        file.close()

#################################################
'''
func use one line stop and path
calculate stop point in which segment of path
then insert the stop point between the two endpoint of the segment
to get a new path
calculate two adjacent point's distence
at last return a linedist obj


与经纬度的计算 需要实际的gps数据(其他来源的数据能够转换也可以使用)
经纬度预先处理过(东经为正,西经为负,北纬为正,南纬为负)

'''
import math


'''
argument: 
    stop ---- one line stops
    path ---- one line path
return value:
    pointarr ---- one line point distance
'''
def insertLineStopToPath(stop,  path):
    pointarr=[]
    #init: set path point to pointarr
    for i in path:
        print(i)
        point=elemOfLineDist(i[0], i[1])
        pointarr.append(point)
    
    #first: insert point
    #stop element: name lng lat
    for i in stop:
        print(i)
        point=elemOfLineDist(i[1], i[2], 0, i[0])
        insertPointToPath(point, pointarr)
        
    #second: calculate distence
    #格式lng1 lat1 dist1 y/n lng2 lat2 dist2 y/n [ ... ]
    for i in range(1, len(pointarr)):
        dist=distOfPointToPoint(pointarr[i-1].getCoordinate(), pointarr[i].getCoordinate())
        pointarr[i-1].setDist(dist)
    return pointarr


def insertPointToPath(point, pointarr):
    min=float('Infinity')
    bias=0
    for i in range(len(pointarr)-1):
        pA=pointarr[i].getCoordinate()
        pB=pointarr[i+1].getCoordinate()
        pC=point.getCoordinate()
        dist=distOfPointToLineSegment(pA, pB, pC)
        print(dist)
        
        if dist<min:
            min=dist
            bias=i
    pointarr.insert(bias+1, point)
    
    return
    
#计算点C到线段AB的距离,点A,B,C中的值都是经纬度
def distOfPointToLineSegment(pA, pB, pC):
    #由于计算的点距离都很近,所以将3个点看成一个平面上
    dist=0
    a=distOfPointToPoint(pA, pB)
    b=distOfPointToPoint(pC, pB)
    c=distOfPointToPoint(pA, pC)
    
    #计算点C到直线AB的距离
    ##x=√(2(a^2 b^2+a^2 c^2+b^2 c^2)-(a^4+b^4+c^4))/2a
    x=math.sqrt(2*(a**2*b**2 + a**2*c**2 + b**2*c**2) - (a**4 + b**4 + c**4)) / (2 * a)
    #print(x)
    
    #判断过点C作的垂线与直线AB的交点D是否在线段AB上
    #计算线段AD和BD的长度,若AD > AB 或 BD > AB,则交点D在不线段AB上
    ##AD^2+x^2=AC^2
    AD=math.sqrt(c**2-x**2)
    BD=math.sqrt(b**2-x**2)
    if AD > a or BD > a:
        dist=min((b, c))
    else:
        dist=x
    return dist

EARTH_RADIUS=6371.004 #单位km
R=EARTH_RADIUS

#计算点A和点B的球面距离,点A,B的值是经纬度
def distOfPointToPoint(pA, pB):
    lngA, latA=float(pA[0]), float(pA[1])
    lngB, latB=float(pB[0]), float(pB[1])
    #预处理
    #北纬取90-纬度值(90- Latitude)，南纬取90+纬度值(90+Latitude)
    #这里都是北纬,也没有南北纬信息用于处理,以后可能会添加
    
    ##角 C = sin(LatA)*sin(LatB) + cos(LatA)*cos(LatB)*cos(MLonA-MLonB)
    C=math.sin(latA)*math.sin(latB)+math.cos(latA)*math.cos(latB)*math.cos(lngA-lngB)
    #print(C)
    dist=R*math.acos(C)*math.pi/180
    return dist

#################################################################

if __name__=='__main__':
    print('test')
    ft = fileTable()
    ft.read_from_file('lines.txt')
    ft.write_to_file('tmp.txt',  'w')
    
    lt=linesTable()
    lt.read_from_file('lines.txt')
    print(lt.getNum())
    for i in range(lt.getNum()):
        print(lt.index(i))
        print(lt.getLineName(i))
        print(lt.getLineUpOrLow(i))
    lt.write_to_file('tmp1.txt', 'w')
    
    lst=lineStopTable()
    lst.read_from_file('linestop.txt')
    for i in range(lst.getNum()):
        print(lst.getOneLineNum(i))
        print(lst.index(i))
        for j in range(lst.getOneLineNum(i)):
            print(lst.getOneStop(lst.index(i), j))
    lst.write_to_file('tmp2.txt', 'w')
    
    lp = linePathTable()
    lp.read_from_file('linepath.txt')
    for i in range(lp.getNum()):
        print(len(lp.index(i)))
        print(lp.index(i))
    lp.write_to_file('tmp3.txt', 'w')
    
    
    ##########################################
    #need test insertLineStopToPath
    ldt=lineDistTable()
    oneline=insertLineStopToPath(lst.index(0), lp.index(0))
    ldt.insertLine(oneline)
    ldt.write_to_file('linedist.txt', 'w')
    
    print('exit')
