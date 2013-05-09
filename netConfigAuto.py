# -*- coding: gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import socket
import network
import time
import sys


config_list = ['1,1,3', 
               '4,1,1,2,24', 
               '2,1,1,301,1վ ����,3վ ����', 
               '2,1,2,302,2վ ����,4վ ����', 
               '2,1,3,304,3վ ����,5վ ����'
               ]

auto_run_demo = ['1,1,1', 
                 '4,1,1,2,24', 
                 ]
auto_run_list = [
                 '2,1,1,301,1վ ����,3վ ����',
                 '2,1,1,301,1վ ����,3վ ����',
                 '2,1,1,301,0վ ����,2վ ����',
                 '2,1,1,301,2վ ����,5վ ����',
                 '2,1,1,301,2վ ����,4վ ����',
                 '2,1,1,301,1վ ����,3վ ����',
                 '2,1,1,301,0վ ����,2վ ����',
                 ]

def netConfigNet(str):
    
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((network.REMOTE_HOST, network.PORT_OF_NETCONFIG))
    sock.send(bytes(str, 'gbk'))
    re=sock.recv(1024)
    print(re)
    return

def netSend():
    for i in config_list:
        netConfigNet(i)
        time.sleep(3)
    
    return

def autoRun():
    
    for i in auto_run_demo:
        netConfigNet(i)
        time.sleep(3)
    i=0
    while i < 10:
        for i in auto_run_list:
            netConfigNet(i)
            time.sleep(5)
        i+=1

if __name__=='__main__':
    
    if len(sys.argv) > 1:
        autoRun()
    else:
        netSend()
