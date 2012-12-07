'''
将电子站牌编号发送给服务端,服务端通过网络对该电子站牌进行配置
暂不提供 命令式操作
'''

import socket
import network

def netConfigNet(str):
    
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((network.REMOTE_HOST, network.PORT_OF_NETCONFIG))
    sock.send(bytes(str, 'gbk'))
    re=sock.recv(1024)
    print(re)
    return

def netConfigClient():
    running=True
    while running:
        s=input('$ ')
        #print(s)
        if s=='q':
            print('exit')
            break
        netConfigNet(s)
    return


if __name__=='__main__':
    netConfigClient()
