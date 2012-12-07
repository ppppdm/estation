'''
公交站信息表:
    表中的一个公交站的信息包含:
    公交站名(或公交站id) 电子站牌编号 线路1 [线路2, ...]
    
    公交站名(或公交站id):
    唯一标识该公交站,建议使用站名(原因是在现场配置电子站牌时公交站名较直接)
    同名的站可以用上行,下行来区别
    
    电子站牌编号:
    电子站牌的唯一标识,见table_IP.py的电子站牌说明
    
    线路1 [线路2, ...]:
    这里线路的数量等于线路总数.
    列出各条线路的名字.线路名字需要在4个字节范围内.即最多4个字母数字或最多2个汉字或最多2个字母数字和1个汉字组合.
    
    示例:
    市政府(上行) 1192 1路 7路 302 游5
    
    提供的操作:
    1.添加一个公交车站信息
    2.通过名字查找一个公交车站的信息
    3.通过编号查找一个公交车站的信息
    4.通过名字修改一个公交车站的编号
'''

BUSSTOPFILE='busStopTable.txt'


class busStopInfo:
    def __init__(self, name='',  num=1, *lines):
        self.name=name
        self.num=num
        self.lines=lines
        return
    
    def getName(self):
        return self.name
    
    def getNum(self):
        return self.num
    
    def getLines(self):
        return self.lines

    def getLineNum(self):
        return len(self.lines)

    def setName(self, name):
        self.name=name
    
    def setNum(self, num):
        self.num=num
        
    def setLines(self, lines):
        self.lines=lines


class table_busStop:
    def __init__(self):
        self.table=[]
        return
    
    def len(self):
        return self.table
    
    def index(self,  index):
        return self.table[index]
    
    def add(self, info):
        ##!!以后需要修改,有同编号的应该覆盖
        self.table.append(info)
        return
    
    def findByName(self, name):
        for info in self.table:
            iname=info.getName()
            if iname==name:
                return info
        return None
    
    def findbyNum(self, num):
        for info in self.table:
            inum=info.getNum()
            if inum==num:
                return info
        return None
    
    def changeNumByName(self, name, num):
        for info in self.table:
            iname=info.getName()
            if iname==name:
                info.setNum(num)
        return
    
    def printTable(self):
        for info in self.table:
            print('%s %d'%(info.getName(), info.getNum()), end='')
            for i in info.getLines():
                print(' %s'%(i), end='')
            print()
    
    def writeToFile(self, filename=BUSSTOPFILE):
        ofile=open(filename,  'w')
        s=''
        for info in self.table:
            s+=info.getName()+'\t'
            s+=str(info.getNum())
            for i in info.getLines():
                s+='\t'+str(i)
            s+='\n'
        ofile.write(s)
        ofile.close()
    
    def readFromFile(self, filename=BUSSTOPFILE):
        infile=open(filename, 'r')
        while True:
            s=infile.readline()
            s=s.rstrip('\n')
            if s=='':
                break
            else:
                arr=s.split('\t')
                print(arr)
                info=busStopInfo(arr[0], int(arr[1])) #直接将lines作为第三个参数传入会出问题,使用setLines
                info.setLines(arr[2:])
                self.add(info)
        infile.close()
        return

if __name__=='__main__':
    def test():
        print('test')
        info = busStopInfo('市政府', 1, '1路', '2路', '302', '游4')
        print(info.getLines())
        info.setLines(('1路', '5路'))
        print(info.getLines())
        info.setLines(('1路', '4路'))
        print(info.getLines())
        
        busstoptable=table_busStop()
        busstoptable.add(info)
        busstoptable.printTable()
        busstoptable.writeToFile()
        busstoptable1=table_busStop()
        busstoptable1.readFromFile()
        busstoptable1.printTable()
        busstoptable1.writeToFile('tmp.txt')
    test()
