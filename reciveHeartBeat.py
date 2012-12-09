# -*- coding: gbk -*-
'''
服务器接收电子站牌的心跳包
    服务器根据协议在指定端口侦听心跳包,同时获取发送心跳包的电子站牌设备的IP地址
    将心跳包和IP地址以数据对的形式发送给IP表维护模块
    
心跳包格式
    长度为4个字节, 例如:
    第1到第4个字节的0x30 0x30 0x30 0x31 代表终端编号是0001
'''


import socket
import network


HOST='localhost'


def reciveHeartBeat(mip):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, network.PORT_OF_HEARTBEAT))
    s.listen(1)
    while True:
        conn, addr=s.accept()
        print('Connected by',  addr)
        data=conn.recv(4)
        if data:
            print(int(data))
            mip.restoreIP(int(data), addr[0])
            conn.sendall(b' ')
        conn.close()
    return


if __name__=='__main__':
    from maintainIP import maintainIP
    from table_IP import table_IP
    import _thread
    def print_ip_table(iptable):
        while True:
            s=input('Enter p to print IP table:')
            if s=='p':
                print('to print')
                break
        
        iptable.writeToFile()
    
    def test():
        iptable=table_IP()
        mip=maintainIP(iptable)
        _thread.start_new_thread(print_ip_table, (iptable, ))
        reciveHeartBeat(mip)
    
    test()
