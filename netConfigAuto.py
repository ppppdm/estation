# -*- coding: gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import socket
import network
import time


config_list = ['1,1,3', 
               '4,1,1,2,25', 
               '2,1,1,301,1站 正常,3站 正常', 
               '2,1,1,302,2站 正常,4站 正常', 
               '2,1,1,304,3站 正常,5站 正常'
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

if __name__=='__main__':
    netSend()
