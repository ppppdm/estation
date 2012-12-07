'''
电子站牌IP地址的表.
    该表表明电子站牌编号与电子站牌的IP地址间一一对应的关系
    电子站牌编号是电子站牌的唯一标识,在电子站牌现场施工时进行配置.
    电子站牌的编号范围是1~9999.
    表由一个长度为10000的数组构成.
    数组的下标表示电子站牌的编号,数组中的内容是对应编号的站牌的IP地址.
    提供以下操作:
    1.修改对应编号的站牌的IP地址
    2.获取对应编号的站牌的IP地址
    3.将整个表写入文件中
'''
import logging


TABLE_LENGTH=10000
INIT_IP='0.0.0.0'
IP_TABLE_FILENAME='IPtable.txt'


class table_IP:
    
    def __init__(self):
        self.table = [INIT_IP] * TABLE_LENGTH
        #logging.basicConfig(level=logging.INFO, 
        #        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',)
        #print(len(self.table))
    
    def setIP(self, num,  ip):
        if num >0 and num <TABLE_LENGTH:
            self.table[num]=ip
            logging.info("set IP %d %s"%(num, ip))
        return
    
    def getIP(self, num):
        if num > 0 and num < TABLE_LENGTH:
            return self.table[num]
        else:
            return INIT_IP
    
    def writeToFile(self,  filename=IP_TABLE_FILENAME):
        outfile=open(filename, 'w')
        for i in self.table:
            outfile.write(i)
            outfile.write('\n')
            outfile.flush()
        outfile.close()
        return
    
    '''读取文件'''
    def readFromFile(self, filename=IP_TABLE_FILENAME):
        infile=open(filename, 'r')
        i=0
        while True:
            s=infile.readline()
            s=s.rstrip('\n')
            if s=='':
                break
            else:
                self.setIP(i, s)
            i+=1
        infile.close()
        return


def test():
    #logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',)
    iptable = table_IP()
    iptable.setIP(1, "192.168.1.0")
    ip = iptable.getIP(1)
    print(ip)
    iptable.writeToFile()
    
    iptable2 = table_IP()
    iptable2.readFromFile()
    iptable2.writeToFile('tmp.txt')
    return

if __name__=='__main__':
    test()
