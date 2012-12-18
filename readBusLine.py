# -*- coding: gbk -*-
import os

BUS_LINE_FLODER='E:\work\estation\lines\\'
LINE_STOP_LIST=list()

class lineBusStop:
    def __init__(self, name=None, line=None, stream=None, start=None, end=None):
        self.name=name
        self.line=line
        self.stream=stream
        ##由于线路文件的站点顺序并不是由起点到终点，因此无法从线路文件中获取线路起点终点信息
        self.start=start
        self.end=end
        return

def addToLineBusList(name, line, stream):
    global LINE_STOP_LIST
    linestop=lineBusStop(name, line, stream)
    LINE_STOP_LIST.append(linestop)
    return

def readFile(filiname):
    file=open(filiname, 'rt')
    #第一行不处理
    file.readline()
    while True:
        str=file.readline()
        str=str.strip('\n')
        if str=='':
            break
        else:
            arr=str.split('\t')
            addToLineBusList(arr[2], arr[0], arr[3])
    file.close()
    return

def readBusLine():
    #lineBusStopList=list()
    files=os.listdir(BUS_LINE_FLODER)
    for i in files:
        readFile(BUS_LINE_FLODER+i)
    return


if __name__=='__main__':
    print('test')
    readBusLine()
    for i in LINE_STOP_LIST:
        print(i.name+' '+i.line+' '+i.stream)
    print('exit')
