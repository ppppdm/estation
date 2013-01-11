# -*- coding: gbk -*-
'''
接收规定格式的站牌发送信息,并信息打包,并根据站id将信息包发送到对应的TCP连接
'''
import threading
import socket
import network
from globalValues import CMD_SET_TOTAL_ROAD
from globalValues import CMD_SET_LINE_TXT
from globalValues import CMD_SET_SPEED
from globalValues import CMD_CLEAR_LINE_TXT
from globalValues import CMD_CLEAR_ALL

from globalValues import CODE_LINE
from globalValues import CODE_TEXT
from globalValues import CODE_CLEAR_TEXT
from globalValues import CODE_SPEED
from globalValues import CODE_CLEAR

from globalValues import CODE_FRAME_HEAD
from globalValues import CODE_FRAME_END
from globalValues import LEN_OF_CODE_CLEAR_TEXT
from globalValues import LEN_OF_CODE_LINE
from globalValues import LEN_OF_CODE_SPEED
from globalValues import LEN_OF_CODE_CLEAR
from utils import crc_check

###########################################
def pack_set_total_road(num):
    data=bytearray(6)
    data[0]=CODE_FRAME_HEAD
    data[1]=CODE_LINE
    data[2]=LEN_OF_CODE_LINE
    data[3]=num
    data[4]=crc_check(data[:-2])
    data[5]=CODE_FRAME_END
    return data

def pack_set_line_txt(r_num, name, msg1, msg2):
    m1len=len(bytes(msg1, 'gbk'))
    m2len=len(bytes(msg2, 'gbk'))
    nlen=len(bytes(name, 'gbk'))
    tlen=m1len+m2len+4+4
    #len of name should less than 4
    if nlen < 4:
        name=name.rjust(4)
    if nlen > 4:
        name=name[0:4]
    data=bytearray(m1len+m2len+9+4)
    data[0]=CODE_FRAME_HEAD
    data[1]=CODE_TEXT
    data[2]=tlen
    data[3]=r_num
    data[4:8]=bytes(name, 'gbk')
    data[8]=m1len
    data[9:9+m1len]=bytes(msg1, 'gbk')
    data[9+m1len]=m2len
    data[10+m1len:-3]=bytes(msg2, 'gbk')
    data[-3]=0x1
    data[-2]=crc_check(data[:-2])
    data[-1]=CODE_FRAME_END
    return data

def pack_set_speed(type, speed, stop):
    data=bytearray(8)
    data[0]=CODE_FRAME_HEAD
    data[1]=CODE_SPEED
    data[2]=LEN_OF_CODE_SPEED
    data[3]=type
    data[4]=speed
    data[5]=stop
    data[-2]=crc_check(data[:-2])
    data[-1]=CODE_FRAME_END
    return data

def pack_clear_line_txt(r_num):
    data=bytearray(6)
    data[0]=CODE_FRAME_HEAD
    data[1]=CODE_CLEAR_TEXT
    data[2]=LEN_OF_CODE_CLEAR_TEXT
    data[3]=r_num
    data[-2]=crc_check(data[:-2])
    data[-1]=CODE_FRAME_END
    return data

def pack_clear_all():
    data=bytearray(5)
    data[0]=CODE_FRAME_HEAD
    data[1]=CODE_CLEAR
    data[2]=LEN_OF_CODE_CLEAR
    data[-2]=crc_check(data[:-2])
    data[-1]=CODE_FRAME_END
    return data

def getCMDandPackageInfo(b_data):
    s_data=str(b_data, 'gbk')
    s_arr=s_data.split('\t')
    cmd=s_arr[0]
    st_id=int(s_arr[1])
    if cmd==CMD_SET_TOTAL_ROAD:
        pack_data=pack_set_total_road(int(s_arr[2]))
    elif cmd==CMD_SET_LINE_TXT:
        pack_data=pack_set_line_txt(int(s_arr[2]), s_arr[3], s_arr[4], s_arr[5])
    elif cmd==CMD_SET_SPEED:
        pack_data=pack_set_speed(int(s_arr[2]), int(s_arr[3]), int(s_arr[4]))
    elif cmd==CMD_CLEAR_LINE_TXT:
        pack_data=pack_clear_line_txt(int(s_arr[2]))
    elif cmd==CMD_CLEAR_ALL:
        pack_data=pack_clear_all()
    return st_id, pack_data

###########################################
class handleSending(threading.Thread):
    def __init__(self, conn, addr, pool):
        threading.Thread.__init__(self)
        self.pool=pool
        self.conn=conn
        self.addr=addr
    
    def run(self):
        print('infoSendingServer Connect by', self.addr)
        b_data=self.conn.recv(1024)
        print(b_data)
        st_id, pack_data=getCMDandPackageInfo(b_data)
        re=self.__send_cmd_TCP(st_id, pack_data, self.pool)
        print(re)
        self.conn.close()
        return

    def __send_cmd_TCP(self, st_id, data, pool):
        try:
            print(st_id, data)
            #从连接池中获取连接,连接可能已经失效
            sock=pool.getConn(st_id)
            if sock==None:
                return
            sock.sendall(data)
            re=sock.recv(1024)
            #连接未失效将连接放回连接池中
            pool.addConn(st_id, sock)
            return re
        except socket.error:
            print('error')
            return None

class infoSendingServer(threading.Thread):
    def __init__(self, pool):
        threading.Thread.__init__(self)
        self.pool=pool
        self.running=True
    
    def run(self):
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((network.HOST, network.PORT_OF_INFOSENDING))
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
    from connectPool import connectPool
    print('test infoSendingServer')
    pool=connectPool()
    infosendingserver=infoSendingServer(pool)
    infosendingserver.start()
