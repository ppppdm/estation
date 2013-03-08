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
from globalValues import BUS_DATA_LEN
from globalValues import BUS_DATA_HEAD
from globalValues import BUS_DATA_END

'''
判断数据完整性和校验,的正确性和数据有效性
返回值0代表出错,1代表正确
'''
def check_data(data):
    if len(data)!=BUS_DATA_LEN:
        print('error data len')
        return 0
    if data[0]!=BUS_DATA_HEAD:
        print('error data head')
        return 0
    if data[-1]!=BUS_DATA_END:
        print('error data end')
        return 0
    if data[-2]!=crc_check(data[1:BUS_DATA_LEN-2]):
        print('error data checksum')
        return 0
    #公交车id判断
    #id=str(data[1:5],'gbk')
    #公交车线路判断
    #line=str(data[5:9],'gbk').strip()
    stream=str(data[9:13], 'gbk')
    if stream !='上行' and stream!='下行':
        print('line stream error, should be 上行 or 下行')
        return 0
    #公交车经纬度判断
    lng=float(str(data[13:21], 'gbk'))/600000
    if lng < 110 or lng > 120:
        print('lng %f error,out bound [110,120]'%lng)
        return 0
    lat=float(str(data[21:29], 'gbk'))/600000
    if lat < 30 or lat >40:
        print('lat %f error,out bound [30,40]'%lat)
        return 0
    return 1

'''
预处理公交车GPS数据为bus_info
'''
def pretreatData(b_data):
    bus=busInfo()
    bus.readDataPackage(b_data[1:BUS_DATA_LEN-2])
    return bus
###########################################

class handleBusData(threading.Thread):
    def __init__(self, conn, addr, cal_handle):
        threading.Thread.__init__(self)
        self.conn=conn
        self.addr=addr
        self.cal_handle=cal_handle
    
    def run(self):
        print('Connected by', self.addr)
        b_data=self.conn.recv(2048)
        print(b_data)
        r_ok=check_data(b_data)
        if r_ok:
            bus_info=pretreatData(b_data)
            self.cal_handle(bus_info)
        self.conn.close()
        return

class busDataServer(threading.Thread):
    def __init__(self, cal_handle):
        threading.Thread.__init__(self)
        self.cal_handle=cal_handle
        self.running=True
        self.thread_arr=[]
        return
    
    def run(self):
        print('busDataServer Start!')
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((network.HOST_OF_BUSGPS, network.PORT_OF_BUSGPS))
        sock.listen(1)
        while self.running:
            conn, addr=sock.accept()
            new_t=handleBusData(conn, addr, self.cal_handle)
            new_t.start()
            self.thread_arr.append(new_t)
        return
    
    def stop(self):
        self.running=False
        for t in self.thread_arr:
            t.join()
