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

auto_run_demo = ['1,1,3', 
                 '4,1,0,2,24', 
                 ]
auto_run_list1 = [
                 '2,1,1,301,1վ ����,6վ ����',
                 '2,1,1,301,1վ ����,5վ ����',
                 '2,1,1,301,0վ ����,4վ ����',
                 '2,1,1,301,3վ ����,7վ ����',
                 '2,1,1,301,2վ ����,5վ ����',
                 '2,1,1,301,1վ ����,3վ ����',
                 '2,1,1,301,0վ ����,2վ ����',
                 ]
auto_run_list2 = [
                 '2,1,2,302,1վ ����,6վ ����',
                 '2,1,2,302,1վ ����,5վ ����',
                 '2,1,2,302,0վ ����,4վ ����',
                 '2,1,2,302,3վ ����,7վ ����',
                 '2,1,2,302,2վ ����,5վ ����',
                 '2,1,2,302,1վ ����,3վ ����',
                 '2,1,2,302,0վ ����,2վ ����',
                 ]
auto_run_list3 = [
                 '2,1,3,304,1վ ����,6վ ����',
                 '2,1,3,304,1վ ����,5վ ����',
                 '2,1,3,304,0վ ����,4վ ����',
                 '2,1,3,304,3վ ����,7վ ����',
                 '2,1,3,304,2վ ����,5վ ����',
                 '2,1,3,304,1վ ����,3վ ����',
                 '2,1,3,304,0վ ����,2վ ����',
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
        time.sleep(5)
    
    j=0
    while j < 10:
        for i in range(len(auto_run_list1)):
            netConfigNet(auto_run_list1[i])
            time.sleep(0.5)
            netConfigNet(auto_run_list2[i])
            time.sleep(0.5)
            netConfigNet(auto_run_list2[i])
            time.sleep(15)
        j += 1

if __name__=='__main__':
    if len(sys.argv) > 1:
        autoRun()
    else:
        netSend()
