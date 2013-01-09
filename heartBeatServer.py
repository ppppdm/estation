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
import threading

###########################################

class handleConnect(threading.Thread):
    def __init__(self, conn, addr, pool):
        threading.Thread.__init__(self)
        self.conn=conn
        self.addr=addr
        self.pool=pool
    
    def run(self):
        print('HeartBeat Connected by',  self.addr)
        data=self.conn.recv(1024)
        print(data)
        try:
            num=int(data[:4])
            self.pool.addConn(num, self.conn)
        except ValueError:
            print('handle Connect error, data %s'%(data[:4]))
        return

class heartBeatServer(threading.Thread):
    def __init__(self, pool):
        threading.Thread.__init__(self)
        self.pool=pool
        self.running=True
    
    def run(self):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((network.HOST_OF_HEARTBEAT, network.PORT_OF_HEARTBEAT))
        s.listen(1)
        while self.running:
            conn, addr=s.accept()
            new_t=handleConnect(conn, addr, self.pool)
            new_t.start()
        return
    
    def stop(self):
        self.running=False
        #同步锁
        print('exit heartBeatServer')

###########################################

if __name__=='__main__':
    #from maintainIP import maintainIP
    #from table_IP import table_IP
    from connectPool import connectPool
    import netConfigServer
    import time
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
        
        heartbeatserver=heartBeatServer(pool)
        heartbeatserver.start()
        
        time.sleep(30)
        heartbeatserver.stop()
    test()
    
