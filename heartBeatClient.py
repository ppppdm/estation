# -*- coding: gbk -*-
'''
heartBeatClient.py ģ���������Ŀͻ���,������˷���������,������һ��' '
����һ�����ԵĿͻ���,HOST��ַ������Ҫ�޸�
�������˲����ͷ�������,Ҳ�������ر�����
'''
import socket
import network
import random

##HOST = socket.gethostbyname(socket.gethostname()) #'pdm1987.vicp.cc'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(network.REMOTE_HOST)
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
