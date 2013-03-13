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

'''
数据测试
完整性：正确(ud)，无数据头(nh)，无数据尾(ne)，数据长度不对(le)
正确性：正确(ud)，校验和出错(ce)
有效性：正确(ud)，线路号(ud)，上下行(ud)，经纬度超范围(ud)
'''

import socket
import network
import threading
from globalValues import BUS_DATA_LEN
from globalValues import BUS_DATA_HEAD
from globalValues import BUS_DATA_END
from utils import crc_check

def sendDataTCP(b_data):
    #print(b_data)
    try:
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print('socket')
        sock.connect((network.REMOTE_HOST, network.PORT_OF_BUSGPS))
        print('connect to', network.REMOTE_HOST, network.PORT_OF_BUSGPS)
        sock.send(b_data)
        #print('send')
        sock.close()
    except Exception as e:
        print('Error!', e, 'in thread', threading.currentThread().ident)
    return

def constructData(id, line, stream, lng, lat):
    b_id=bytes(id, 'gbk')
    b_line=bytes(line.rjust(4), 'gbk')
    b_stream=bytes(stream, 'gbk')
    b_lng=bytes(lng, 'gbk')
    b_lat=bytes(lat, 'gbk')
    
    if len(b_id)!=4:
        print('bus id len should be 4')
        return b''
    if len(b_line)>4:
        print('line name should less than 5')
        return b''
    if len(b_stream)!=4:
        print('line stream should be 上行 or 下行')
        return b''
    if len(b_lng)!=8 or len(b_lat)!=8:
        print('len of lng/lat should be 8')
        return b''
    
    data=bytearray(BUS_DATA_LEN)
    data[0]=BUS_DATA_HEAD
    data[1:5]=b_id
    data[5:9]=b_line
    data[9:13]=b_stream
    data[13:21]=b_lng
    data[21:29]=b_lat
    data[-2]=crc_check(data[1:-2])
    data[-1]=BUS_DATA_END
    return data
