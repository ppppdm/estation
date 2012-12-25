# -*- coding: gbk -*-
'''
busDataServer.py 接收公交公司的公交车GPS数据.
服务接口需要对公交数据中心公布,方便将数据发送过来.

busDataServer.py 启动后一直读取服务端口传来的数据.
并将数据
    1.写入到文件中
    2.调用后台处理程序处理
    
busDataServer.py 启动直到电子站牌主控程序通知其关闭或系统当机.
所以连接 busDataServer 的程序在 busDataServer 关闭后对异常忽略并再次发起连接请求.

'''

import socket
import network
import threading
from utils import crc_check
from busCalculate import busInfo
'''
from busCalculate import updateLineBus
from busCalculate import lineBusTable
from busCalculate import busInfoTable
from lineDistance import lineDistTable
from lineDistance import linesTable
'''

from globalValues import BUS_DATA_LEN
from globalValues import BUS_DATA_HEAD
from globalValues import BUS_DATA_END

FILENAME='busData.txt'
file=None


def write_to_file(businfo):
    try:
        file=open(FILENAME, 'w')
    except IOError:
        print('open file error')
    else:
        print('open file ok')
    s=''
    s+=businfo.id+'\t'+str(businfo.lineName)+'\t'+str(businfo.lng)+'\t'+str(businfo.lat)+'\n'
    file.write(s)
    file.flush()
    file.close()
    return

def printRet(businfo):
    s=businfo.id+'\t'+str(businfo.lineName)+'\t'+str(businfo.lng)+'\t'+str(businfo.lat)
    print(s)

'''
判断数据完整性和校验,的正确性和数据有效性
'''
def check_data(data):
    if len(data)!=BUS_DATA_LEN:
        print('error data len')
        return
    if data[0]!=BUS_DATA_HEAD:
        print('error data head')
        return
    if data[-1]!=BUS_DATA_END:
        print('error data end')
        return
    if data[-2]!=crc_check(data[1:BUS_DATA_LEN-2]):
        print('error data checksum')
        return
    #公交车id判断
    #id=str(data[1:5],'gbk')
    #公交车线路判断
    #line=str(data[5:9],'gbk').strip()
    stream=str(data[9:13], 'gbk')
    if stream !='上行' and stream!='下行':
        print('line stream error, should be 上行 or 下行')
        return
    #公交车经纬度判断
    lng=float(str(data[13:21], 'gbk'))/600000
    if lng < 110 or lng > 120:
        print('lng %f error,out bound [110,120]'%lng)
        return
    lat=float(str(data[21:29], 'gbk'))/600000
    if lat < 30 or lat >40:
        print('lat %f error,out bound [30,40]'%lat)
        return
    
    bus=busInfo()
    bus.readDataPackage(data[1:BUS_DATA_LEN-2])
    return bus

'''
接收并预处理公交车GPS数据,不向发送发返回结果
规定公交车GPS数据包格式如下：
    数据头 公交车ID 所属线路 经纬度 校验和 数据尾
    数据头：长度1字节,0x55
    公交车ID：长度4字节，ASCII表示
    所属线路：长度4字节，ASCII表示
    线路上下行：长度4字节
    经纬度：16字节，前8个字节为经度，后8个字节为纬度
    校验和：长度1字节，公交车ID，所属线路和经纬度按位异或的结果
    数据尾：长度1字节，0xaa
数据总长度为27个字节
预处理判断数据校验和是否正确
'''
'''
lt=linesTable()
lt.read_from_file('lines.txt')

ldt=lineDistTable()
ldt.read_from_file('linedist.txt')

lbt=lineBusTable()
lbt.read_from_dist_file('linedist.txt')

bit=busInfoTable()

def handleBusData(conn, addr):
    print('Connected by ',  addr)
    data=conn.recv(2048)
    print(data)
    ret=check_data(data)
    if ret != None:
        write_to_file(ret)
        printRet(ret)
        #updateLineBus(lineTable, lineDistTable, lineBusTable, busInfoTable, busInfo)
        #updateLineBus(lt, ldt, lbt,bit,ret)
    conn.close()
    return
'''
class handleBusData(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn=conn
        self.addr=addr
    
    def run(self):
        print('Connected by', self.addr)
        
        data=self.conn.recv(2048)
        print(data)
        ret=check_data(data)
        if ret!=None:
            printRet(ret)
        self.conn.close()
        return

def busDataServer(flag):
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((network.HOST_OF_BUSGPS, network.PORT_OF_BUSGPS))
    sock.listen(1)
    while True:
        conn, addr=sock.accept()
        new_t=handleBusData(conn, addr)
        new_t.start()
        #print(new_t)
    return

class busDataServer(threading.Thread):
    def __init__(self, ):
        return

if __name__=='__main__':
    busDataServer(0)
