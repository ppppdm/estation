# -*- coding: gbk -*-
'''
infoSending提供对外的接口
'''

import socket
import network

def __infoSendToServer(str):
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((network.REMOTE_HOST, network.PORT_OF_NETCONFIG))
    sock.send(bytes(str, 'gbk'))
    re=sock.recv(1024)
    sock.close()
    return re


def send_line(num, No, pool):

    return

def send_text(R_No, name, msg1, msg2, No, pool):

    return

def send_clear_text(R_No, No, pool):

    return

#显示方式,速度,停留时间设置
def send_speed(type, speed, stop, No, pool):

    return

#清除屏幕
def send_clear(No, pool):

    return
