# -*- coding: gbk -*-
# auther : pdm
# email : ppppdm@gmail

import readBusLine

BUSSTOPLIST=list()

class busStopLines:
    def __init__(self, name, stream):
        self.name=name
        self.stream=stream

class busStop:
    def __init__(self, name=None):
        self.name=name
        self.lines=list()
        return

def findByStopName(list, name):
    sl=[]
    for i in list:
        if i.name==name:
            sl.append(i)
    return sl

def findLineByName(lines, name):
    for i in lines:
        if i[0]==name:
            return i
    return None

def createBusStopList(stoplist):
    for i in stoplist:
        stop=findByStopName(BUSSTOPLIST, i.name)
        if len(stop)==0:
            bsl=(i.line, i.stream)
            bs=busStop(i.name)
            bs.lines.append(bsl)
            BUSSTOPLIST.append(bs)
        elif len(stop)==1:
            ## stop could has 0 line
            if len(stop[0].lines)==0:
                bsl=(i.line, i.stream)
                stop[0].lines.append(bsl)
            elif stop[0].lines[0][1]==i.stream:
                ##line impossabel has two same stop
                bsl=(i.line, i.stream)
                stop[0].lines.append(bsl)
            else: 
                bsl=(i.line, i.stream)
                bs=busStop(i.name)
                bs.lines.append(bsl)
                BUSSTOPLIST.append(bs)
        else:
            if stop[0].lines[0][1]==i.stream:
                bsl=(i.line, i.stream)
                stop[0].lines.append(bsl)
            else:
                bsl=(i.line, i.stream)
                stop[1].lines.append(bsl)
    return

def getSerialNumber(name, line, stream):
    i=1
    for stop in BUSSTOPLIST:
        if stop.name==name:
            for l in stop.lines:
                if l ==(line, stream):
                    return i
        i+=1
    return -1

def getStopInfoByName(name):
    s=''
    i=0
    for stop in BUSSTOPLIST:
        if stop.name==name:
            s+=stop.name+'\t'+str(i)+'\t'
            for line in stop.lines[:-1]:
                s+=line[0]+'\t'+line[1]+'\t'
            s+=stop.lines[-1][0]+'\t'+stop.lines[-1][1]+'\n'
        i+=1
    return s

def getLineTotalNum(sn):
    return len(BUSSTOPLIST[sn].lines)

def getLineNoInStop(sn, line):
    lines=BUSSTOPLIST[sn].lines
    No=0
    for i in lines:
        if i[0]==line:
            return No
        No+=1
    return -1

def writeBusStopTable(filename, busstoplist):

    file=open(filename, 'wt')
    s=''
    for i in busstoplist:
        s+=i.name+'\t'
        for j in i.lines:
            s+=j[0]+'\t'+j[1]+'\t'
        s.strip('\t')
        s+='\n'
    file.write(s)
    file.close()
    return

def readBusStopTable(filename, busstoplist):
    file=open(filename, 'r')
    
    while True:
        s=file.readline()
        s=s.strip('\n')
        if s=='':
            break
        else:
            arr=s.split('\t')
            bs=busStop(arr[0])
            for i in range(1, len(arr[1:]) , 2):
                bsl=(arr[i], arr[i+1])
                bs.lines.append(bsl)
            busstoplist.append(bs)
    file.close()
    return

if __name__=='__main__':
    print('test')
    
    readBusLine.readBusLine()
    createBusStopList(readBusLine.LINE_STOP_LIST)
    
    for i in BUSSTOPLIST:
        print(i.name, end=' ')
        print(i.lines)
    
    ##write to file
    filename='stopTable.txt'
    file=open(filename, 'wt')
    s=''
    for i in BUSSTOPLIST:
        s+=i.name+'\t'
        for j in i.lines:
            s+=j[0]+'\t'+j[1]+'\t'
        s.strip('\t')
        s+='\n'
    file.write(s)
    file.close()
    
    tmp=[]
    readBusStopTable('stopTable.txt', tmp)
    writeBusStopTable('tmp8.txt', tmp)
    
    print(getSerialNumber('市公交调度中心', '202', '下行'))
    print(getSerialNumber('市公交调度中心', '202', '上行'))
    print(getSerialNumber('实验小学黄河分校', '302', '下行'))
    print(getStopInfoByName('市公交调度中心'))
    print(getLineTotalNum(23))
    print(getLineNoInStop(23, '402'))

    print('exit')
