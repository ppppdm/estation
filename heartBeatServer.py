# -*- coding: gbk -*-
'''
服务器接收电子站牌的心跳包
    服务器根据协议在指定端口侦听心跳包,同时获取发送心跳包的电子站牌设备的IP地址
    将心跳包和IP地址以数据对的形式发送给IP表维护模块
    
心跳包格式
    长度为4个字节, 例如:
    第1到第4个字节的0x30 0x30 0x30 0x31 代表终端编号是0001
    
服务接收参数p打印iptable到文件中
'''


import socket
import network
import _thread


def handleConnect(conn, pool):
    data=conn.recv(1024)
    print(data)
    num=0
    try:
        num=int(data[:4])
    except ValueError:
        print('handle Connect error, data %s'%(data[:4]))
    pool.addConn(num, conn)
    return

def reciveHeartBeat(pool):
    print(network.HOST_OF_HEARTBEAT)
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((network.HOST_OF_HEARTBEAT, network.PORT_OF_HEARTBEAT))
    s.listen(1)
    while True:
        conn, addr=s.accept()
        print('HeartBeat Connected by',  addr)
        t_id=_thread.start_new_thread(handleConnect, (conn, pool))
        print('handle connect thread id %d'%(t_id))
    return


if __name__=='__main__':
    #from maintainIP import maintainIP
    #from table_IP import table_IP
    from connectPool import connectPool
    import netConfigServer
    '''
    测试程序申请一个ip table, 并启动接收reciveHeartBeat服务
    服务将接收到的ip 写入到ip table中
    '''
    
    def test():
        #iptable=table_IP()
        #mip=maintainIP(iptable)
        pool=connectPool()
        #conn=None
        #_thread.start_new_thread(handleConnect, (conn, pool))
        _thread.start_new_thread(netConfigServer.netConfigServer, (pool, ))
        
        reciveHeartBeat(pool)
    
    test()
