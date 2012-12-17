# -*- coding: gbk -*-
'''
向busDataServer发送公交车数据
规定公交车GPS数据包格式如下：
    数据头 公交车ID 所属线路 经纬度 校验和 数据尾
    数据头：长度1字节,0x55
    公交车ID：长度4字节，ASCII表示
    所属线路：长度4字节，ASCII表示
    经纬度：16字节，前8个字节为经度，后8个字节为纬度
    校验和：长度1字节，公交车ID，所属线路和经纬度按位异或的结果
    数据尾：长度1字节，0xaa
数据总长度为27个字节
'''

import socket
import network

def crc_check(b_data):
    if len(b_data)==0:
        return 0
    crc=b_data[0]
    for i in b_data[1:]:
        crc^=i
    return crc

def busDataClient():
    bus_id=bytes(str(7023), 'utf8')
    line=bytes(str(303).rjust(4), 'utf8')
    lng=bytes(str(70922263), 'utf8')
    lat=bytes(str(20374106), 'utf8')
    
    data=bytearray(27)
    data[0]=0x55
    data[1:5]=bus_id
    data[5:9]=line
    data[9:17]=lng
    data[17:25]=lat
    data[25]=crc_check(data[1:25])
    data[26]=0xaa
    
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
