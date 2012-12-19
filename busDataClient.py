# -*- coding: gbk -*-
'''
向busDataServer发送公交车数据
规定公交车GPS数据包格式如下：
    数据头 公交车ID 所属线路 经纬度 校验和 数据尾
    数据头：长度1字节,0x55
    公交车ID：长度4字节，ASCII表示
    所属线路：长度4字节，ASCII表示
    线路上下行：长度4字节
    经纬度：16字节，前8个字节为经度，后8个字节为纬度
    校验和：长度1字节，公交车ID，所属线路和经纬度按位异或的结果
    数据尾：长度1字节，0xaa
数据总长度为31个字节
'''

import socket
import network
from globalValues import BUS_DATA_LEN

def crc_check(b_data):
    if len(b_data)==0:
        return 0
    crc=b_data[0]
    for i in b_data[1:]:
        crc^=i
    return crc

def busDataClient():
    bus_id=bytes(str(7023), 'gbk')
    line=bytes(str('303').rjust(4), 'gbk')
    stream=bytes('上行', 'gbk')
    lng=bytes(str(70922263), 'gbk')
    lat=bytes(str(20374106), 'gbk')
    
    data=bytearray(BUS_DATA_LEN)
    data[0]=0x55
    data[1:5]=bus_id
    data[5:9]=line
    data[9:13]=stream
    data[13:21]=lng
    data[21:29]=lat
    data[-2]=crc_check(data[1:-2])
    data[-1]=0xaa
    
    print(data)
    print(data[1:25])
    
    try:
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('socket')
        sock.connect((network.REMOTE_HOST, network.PORT_OF_BUSGPS))
        print('connect')
        sock.send(data)
        print('send')
        sock.close()
    except:
        print('error')
    print('exit')
    return

if __name__=='__main__':
    busDataClient()
