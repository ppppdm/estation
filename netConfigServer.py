'''
netConfigServer.py 接收控制客户端的控制命令,根据命令配置对于的电子站牌客户端.
控制命令组成:
    电子站牌的编号
配置方法:
    根据控制命令中的编号到busStop table中找到相应的busStop info.
    并根据编号在IP table中找到对应的IP地址
    向该IP地址发送配置命令
    1.配置线路总数
    根据busStop中线路总数和电子站牌LED通信协议配置电子站牌
    
    
    需要修改,ip地址参数不需要,改为根据编号去获取连接
'''

import socket
import network

CODE_TEXT           =0xC1
CODE_VOICE          =0xC2
CODE_CLEAR_TEXT =0xC3
CODE_CLEAR_VOICE=0xC4
CODE_HEART	       =0xC5
CODE_LINE		       =0xC6
CODE_SPEED          =0xC7
CODE_CHECK          =0xC8
CODE_TIME		       =0xC9
CODE_PERH	           =0xCA
CODE_TEMP	       =0xCB
CODE_CLEAR          =0xCC
CODE_PERH1	       =0xCD

CODE_FRAME_HEAD =0xF1
CODE_FRAME_END   =0xAA

LEN_OF_CODE_LINE=0X1
LEN_OF_CODE_CLEAR_TEXT=0x1
LEN_OF_CODE_SPEED=0x3

def crc_check(b_data):
    if len(b_data)==0:
        return 0
    crc=b_data[0]
    for i in b_data[1:]:
        crc^=i
    return crc

#根据设备编号到连接池中找到该连接
def send_cmd_TCP(data, No, pool):
    try:
        print(data)
        #sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.connect((ip,  network.TCP_PORT_OF_LED))
        #从连接池中获取连接,连接可能已经失效
        sock=pool.getConn(No)
        if sock==None:
            return
        print('connect OK')
        sock.sendall(data)
        print('send OK')
        sock.settimeout(5)
        re=sock.recv(1024)
        print('recive OK')
        
        #连接未失效将连接放回连接池中
        pool.addConn(No, sock)
        return re
    except socket.error:
        print(sock)
        return

def send_line(num, No, pool):
    print('send_line')
    data=bytearray(6)
    data[0]=CODE_FRAME_HEAD
    data[1]=CODE_LINE
    data[2]=LEN_OF_CODE_LINE
    data[3]=num
    data[4]=crc_check(data[:-2])
    data[5]=CODE_FRAME_END
    
    re=send_cmd_TCP(data, No, pool)
    print(re)
    return

def send_text(R_No, name, msg1, msg2, No, pool):
    print('send_txt')
    m1len=len(msg1)
    m2len=len(msg2)
    nlen=len(name)
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
    data[3]=R_No
    data[4:8]=bytes(name, 'utf8')
    data[8]=m1len
    data[9:9+m1len]=bytes(msg1, 'utf8')
    data[9+m1len]=m2len
    data[10+m1len:-3]=bytes(msg2, 'utf8')
    data[-3]=0x1
    data[-2]=crc_check(data[:-2])
    data[-1]=CODE_FRAME_END
    
    re=send_cmd_TCP(data, No, pool)
    print(re)
    return

def send_clear_text(R_No, No, pool):
    print('send_clear_text')
    data=bytearray(6)
    data[0]=CODE_FRAME_HEAD
    data[1]=CODE_CLEAR_TEXT
    data[2]=LEN_OF_CODE_CLEAR_TEXT
    data[3]=R_No
    data[-2]=crc_check(data[:-2])
    data[-1]=CODE_FRAME_END
    
    re=send_cmd_TCP(data, No, pool)
    print(re)
    return

#显示方式,速度,停留时间设置
def send_speed(type, speed, stop, No, pool):
    print('send_speed')
    data=bytearray(8)
    data[0]=CODE_FRAME_HEAD
    data[1]=CODE_SPEED
    data[2]=LEN_OF_CODE_SPEED
    data[3]=type
    data[4]=speed
    data[5]=stop
    data[-2]=crc_check(data[:-2])
    data[-1]=CODE_FRAME_END
    
    re=send_cmd_TCP(data, No, pool)
    print(re)
    return

#清除屏幕
def send_clear():
    return

import time
def netConfigServer(pool, bustop):
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((network.HOST, network.PORT_OF_NETCONFIG))
    sock.listen(1)
    while True:
        conn, addr=sock.accept()
        print('Connected by',  addr)
        data=conn.recv(1024)
        if data:
            print(data)
            conn.sendall(network.NET_RET_OK)
            s=str(data, 'utf8')
            arr=s.split()
            if arr[0]=='1':
                #test code here
                send_line(int(arr[1]), 1, pool)
                time.sleep(5)
            if arr[0]=='2':
                arr[2]=arr[2].strip('\'')
                arr[3]=arr[3].strip('\'')
                arr[4]=arr[4].strip('\'')
                send_text(int(arr[1]), arr[2],arr[3], arr[4], 1,  pool)
            if arr[0]=='3':
                 send_clear_text(int(arr[1]), 1, pool)
            if arr[0]=='4':
                 send_speed(int(arr[1]), int(arr[2]), int(arr[3]), 1, pool)
        conn.close()
    return


if __name__=='__main__':
    print('test')
    #from table_busStop import table_busStop
    #from table_IP import table_IP
    #from connectPool import coonectPool
    #pool=connectPool()
    #ip_table=table_IP()
    #ip_table.readFromFile()
    #eNo=1
    
    #busstop_table=table_busStop()
    #busstop_table.readFromFile()
    #netConfigServer(ip_table, busstop_table)
    #just test send_line function
    #ip=ip_table.getIP(1)
    #send_line(3, eNo, pool)
    #send_text(R_No, name, msg1, msg2, No, pool):
    send_text(1, '104', 'fff', 'xxx', 1, None)

    
