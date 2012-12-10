# -*- coding: gbk -*-
'''
busStopServer 配置服务
busStopServer.py 接收busStop Info,并将busStop Info储存到busStopTable中.
busStopTable的定义见table_busStop.py
'''

import socket
import network
import _thread
from table_busStop import busStopInfo

RUNNING=True

def busStopServerInput():
    global RUNNING
    
    while True:
        s=input()
        if s=='q':
            RUNNING=False
            break
    exit()
    return


def busStopServer(t_stop):
    global RUNNING
    _thread.start_new_thread(busStopServerInput, ())
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((network.HOST, network.PORT_OF_BUSSTOP))
    s.listen(1)
    while RUNNING:
        conn, addr=s.accept()
        print('Connected by',  addr)
        data=conn.recv(1024)
        if data:
            print(data)
            sdata=data.decode('utf8')
            print(sdata)
            arr=sdata.split()
            info=busStopInfo(arr[0], int(arr[1])) #直接将lines作为第三个参数传入会出问题,使用setLines
            info.setLines(arr[2:])
            t_stop.add(info)
            #测试时将table写入到文件中,非测试时注释掉
            t_stop.writToFile()
            conn.sendall(network.NET_RET_OK)
        print(RUNNING)
        conn.close()
    return


if __name__=='__main__':
    from table_busStop import table_busStop
    def test():
        
        print('test')
        t_stop=table_busStop()
        busStopServer(t_stop)
        return
    
    test()
