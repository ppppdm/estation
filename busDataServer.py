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
import atexit
import _thread
from busCalculate import busInfo

FILENAME='busData.txt'
file=None


def exit_server():
    global file
    file.close()
    return


def write_to_file(data):
    file.write(data)
    file.flush()
    return

funclist=[write_to_file]

def crc_check(b_data):
    if len(b_data)==0:
        return 0
    crc=b_data[0]
    for i in b_data[1:]:
        crc^=i
    return crc

'''
判断数据完整性和校验和的正确性
'''
def check_data(data):
    '''
    先找到数据头
    '''
    i=0
    while i < len(data):
        if data[i]==0x55:
            '''再找数据尾'''
            if data[i+BUS_DATA_LEN-1]==0xaa:
                '''判断校验和'''
                checksum=data[i+BUS_DATA_LEN-2]
                cc=crc_check(data[i+1:i+BUS_DATA_LEN-2])
                if cc == checksum:
                    bus=busInfo()
                    bus.readDataPackage(data[i+1:i+BUS_DATA_LEN-2])
                    return bus
                else:
                    return None
            else:
                return None
        i+=1
    
    return None

'''
接收并预处理公交车GPS数据,不向发送发返回结果
规定公交车GPS数据包格式如下：
    数据头 公交车ID 所属线路 经纬度 校验和 数据尾
    数据头：长度1字节,0x55
    公交车ID：长度4字节，ASCII表示
    所属线路：长度4字节，ASCII表示
    经纬度：16字节，前8个字节为经度，后8个字节为纬度
    校验和：长度1字节，公交车ID，所属线路和经纬度按位异或的结果
    数据尾：长度1字节，0xaa
数据总长度为27个字节
预处理判断数据校验和是否正确
'''
BUS_DATA_LEN=27
def handleBusData(conn, addr, dofunc):
    print('Connected by ',  addr)
    '''
    接收数据
    '''
    data=conn.recv(2048)
    '''
    检查数据
    '''
    ret=check_data(data)
    if ret != None:
        dofunc(data)
    conn.close()
    return

'''
参数:
    flag:0 写到文件 1.调用函数
'''
def busDataServer(flag):
    global file
    running=True
    
    dofunc=funclist[flag]
    
    try:
        file=open(FILENAME, 'ab')
    except IOError:
        print('open file error')
    else:
        print('open file ok')
        atexit.register(exit_server)
    
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((network.HOST_OF_BUSGPS, network.PORT_OF_BUSGPS))
    sock.listen(1)
    while running:
        conn, addr=sock.accept()
        _thread.start_new_thread(handleBusData, (conn, addr, dofunc))
    return


if __name__=='__main__':
    busDataServer(0)
