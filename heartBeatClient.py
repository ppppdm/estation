# -*- coding: gbk -*-
'''
heartBeatClient.py 模拟心跳包的客户端,给服务端发送心跳包,并接收一个' '
'''
import socket
import network
import random

HOST = 'pdm1987.vicp.cc'    # The remote host
PORT = 2005              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,network.PORT_OF_HEARTBEAT))
a=random.randint(1, 9999)
stra=str(a)
print(stra)
print(bytes(stra, 'utf-8'))

s.sendall(bytes(stra, 'utf-8'))
data = s.recv(1024)
s.close()
print('Received', repr(data)+'##')
