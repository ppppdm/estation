# -*- coding: gbk -*-
'''
heartBeatClient.py 模拟心跳包的客户端,给服务端发送心跳包,并接收一个' '
这是一个测试的客户端,HOST地址根据需要修改
服务器端不发送返回数据,也不主动关闭连接
'''
import socket
import network
import random

##HOST = socket.gethostbyname(socket.gethostname()) #'pdm1987.vicp.cc'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((network.REMOTE_HOST,network.PORT_OF_HEARTBEAT))
a=random.randint(1, 9999)
stra=str(a)
print(stra)
print(bytes(stra, 'gbk'))
s.sendall(bytes(stra, 'gbk'))
##data = s.recv(1024)
##print('Received', repr(data)+'##')
s.close()
print('exit')
