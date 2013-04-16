# -*- coding: gbk -*-
'''
network.py�����˷���������Ľӿں�Э��
'''
import socket
import os
try:
    test=os.environ['TEST']
except KeyError:
    test=0

#host,ע�������host������'localhost'��'127.0.0.1'
#HOST �Ǳ�����ַ,�ɷ���˺Ͳ��Կͻ���ʹ��
#REMOTE_HOST �ɿͻ���ʹ��
HOST=socket.gethostbyname(socket.gethostname())
#remote host
REMOTE_HOST='pdm1987.vicp.cc'
if test:
    REMOTE_HOST=socket.gethostbyname(socket.gethostname())

#host of recive heartbeat
HOST_OF_HEARTBEAT=HOST
#port of recive heartbeat
PORT_OF_HEARTBEAT=2001
#host of recive bus gps infomaiton
HOST_OF_BUSGPS=HOST
#port of recive bus gps infomaiton
PORT_OF_BUSGPS=2002
#host of recive bus stop infomation
HOST_OF_BUSSTOP=HOST
#port of recive bus stop infomation
PORT_OF_BUSSTOP=2003
#host of net config estation
HOST_OF_NETCONFIG=HOST
#port of net config estation
PORT_OF_NETCONFIG=2004
#host of net config estation
HOST_OF_INFOSENDING=HOST
#port of net config estation
PORT_OF_INFOSENDING=2005
#host of recive bus user control infomation
HOST_OF_USERCONTROL=HOST
#port of recive bus user control infomation
PORT_OF_USERCONTROL=2006

#tcp port of LED
TCP_PORT_OF_LED=8777
#udp port of LED
UDP_PORT_OF_LED=8787

#network return Ok
NET_RET_OK=b'1'
#network return Failure
NET_RET_FAILURE=b'0'
