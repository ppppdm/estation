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
from globalValues import BUS_DATA_LEN
from globalValues import BUS_DATA_HEAD
from globalValues import BUS_DATA_END
from utils import crc_check

def sendDataTCP(b_data):
    print(b_data)
    try:
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print('socket')
        sock.connect((network.REMOTE_HOST, network.PORT_OF_BUSGPS))
        #print('connect')
        sock.send(b_data)
        #print('send')
        sock.close()
    except:
        print('error')
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

def busDataClient():
    bus_id=str(7023)
    line='303'
    stream='上行'
    lng=str(70922263)
    lat=str(20374106)
    
    data=constructData(bus_id, line, stream, lng, lat)
    
    sendDataTCP(data)
    print('exit')
    return

#################TEST####################
from globalValues import USE_DATA
from globalValues import NO_HEAD
from globalValues import NO_END
from globalValues import LEN_ERR
from globalValues import CHK_ERR

TEST_FILE='test/busGPS_test.txt'

def switchByArg(arr):
    arg=arr[0]
    b_data=b''
    if arg==USE_DATA:
        print(USE_DATA)
        b_data=constructData(arr[1], arr[2], arr[3], arr[4], arr[5])
        sendDataTCP(b_data)
    elif arg== NO_HEAD:
        print(NO_HEAD)
        b_data=constructData(arr[1], arr[2], arr[3], arr[4], arr[5])
        b_data[0]=0
        sendDataTCP(b_data)
    elif arg==NO_END:
        print(NO_END)
        b_data=constructData(arr[1], arr[2], arr[3], arr[4], arr[5])
        b_data[-1]=0
        sendDataTCP(b_data)
    elif arg==LEN_ERR:
        print(LEN_ERR)
        b_data=constructData(arr[1], arr[2], arr[3], arr[4], arr[5])
        b_data+=b'x'
        sendDataTCP(b_data)
    elif arg==CHK_ERR:
        print(CHK_ERR)
        b_data=constructData(arr[1], arr[2], arr[3], arr[4], arr[5])
        b_data[-2]^=1
        sendDataTCP(b_data)
    return

def readTestFile():
    '''从文件中读取测试数据并构造要发送的数据'''
    file =open(TEST_FILE, 'r')
    while True:
        ss=file.readline()
        ss=ss.strip('\n')
        if ss=='':
            break
        arr=ss.split('\t')
        switchByArg(arr)
    file.close()
    return
#########################################

if __name__=='__main__':
    import os
    try:
        test=os.environ['TEST_GPS']
    except KeyError:
        test=0
    if test:
        readTestFile()
    busDataClient()
