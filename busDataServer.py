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

FILENAME='busData.txt'
file=None


def exit_server():
    global file
    file.close()
    return


def write_to_file(data):
    file.write(data)
    return


funclist=[write_to_file]

'''
参数:
    flag:0 写到文件 1.调用函数
'''
def busDataServer(flag):
    global file
    running=True
    
    dofunc=funclist[flag]
    
    try:
        file=open(FILENAME, 'a')
    except IOError:
        print('open file error')
    else:
        print('open file ok')
        atexit.register(exit_server)
    
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((network.HOST_OF_BUSDATA, network.PORT_OF_BUSDATA))
    sock.listen(1)
    while running:
        conn, addr=sock.accept()
        print('Connected by ',  addr)
        data=conn.recv(2048)
        dofunc(data)
        conn.close()
    return


if __name__=='__main__':
    busDataServer(0)
