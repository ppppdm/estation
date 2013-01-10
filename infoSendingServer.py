# -*- coding: gbk -*-
'''
接收规定格式的站牌发送信息,并信息打包,并根据站id将信息包发送到对应的TCP连接
'''
import threading.Thread
import socket
import network

class handleSending(threading.Thread):
    def __init__(self, conn, addr, pool):
        self.pool=pool
        self.conn=conn
        self.addr=addr
    
    def run(self):
        
        return


class infoSendingServer(threading.Thread):
    def __init__(self, pool):
        threading.Thread.__init__(self)
        self.pool=pool
        self.running=True
    
    def run(self):
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((network.HOST, network.PORT_OF_NETCONFIG))
        sock.listen(1)
        while self.running:
            conn, addr=sock.accept()
            new_t=handleSending(conn, addr, self.pool)
            new_t.start()
        return
    
    def stop(self):
        self.running=False
        print('exit infoSendingServer')



if __name__=='__main__':
    print('test infoSendingServer')
