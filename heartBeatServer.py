# -*- coding: gbk -*-
'''
���������յ���վ�Ƶ�������
    ����������Э����ָ���˿�����������,ͬʱ��ȡ�����������ĵ���վ���豸��IP��ַ
    ����������IP��ַ�����ݶԵ���ʽ���͸�IP��ά��ģ��
    
��������ʽ
    ����Ϊ4���ֽ�, ����:
    ��1����4���ֽڵ�0x30 0x30 0x30 0x31 �����ն˱����0001
    
������ղ���p��ӡiptable���ļ���
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
        #ͬ����
        print('exit heartBeatServer')

###########################################

if __name__=='__main__':
    from connectPool import connectPool
    import netConfigServer
    import time
    '''
    ���Գ�������һ��ip table, ����������reciveHeartBeat����
    ���񽫽��յ���ip д�뵽ip table��
    '''
    
    def test():
        pool=connectPool()
        _thread.start_new_thread(netConfigServer.netConfigServer, (pool, ))
        
        heartbeatserver=heartBeatServer(pool)
        heartbeatserver.start()
        
        time.sleep(30)
        #heartbeatserver.stop()
    test()
    
