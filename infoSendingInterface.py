# -*- coding: gbk -*-
'''
infoSending提供对外的接口
'''

import socket
import network
from globalValues import CMD_SET_TOTAL_ROAD
from globalValues import CMD_SET_LINE_TXT
from globalValues import CMD_SET_SPEED
from globalValues import CMD_CLEAR_LINE_TXT
from globalValues import CMD_CLEAR_ALL

def __infoSendToServer(s_data):
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((network.REMOTE_HOST, network.PORT_OF_INFOSENDING))
    sock.send(bytes(s_data, 'gbk'))
    re=sock.recv(1024)
    sock.close()
    return re

#设置公交站线路总数
#参数：st_id 公交站编号，num 线路总数
def set_total_road(st_id, total):
    s_data=CMD_SET_TOTAL_ROAD+'\t'+str(st_id)+'\t'+str(total)
    __infoSendToServer(s_data)
    return

#设置电子站牌信息
#参数：st_id 公交站编号，r_num 线路在该站编号，r_name 线路名，msg1 上屏信息，msg2 下屏信息
def set_line_text(st_id, r_num, r_name, msg1, msg2):
    s_data=CMD_SET_LINE_TXT+'\t'+str(st_id)+'\t'+str(r_num)+'\t'+str(r_name)+'\t'+str(msg1)+'\t'+str(msg2)
    __infoSendToServer(s_data)
    return

#清除站牌某路信息
#参数：st_id 公交站编号，r_num 线路在该站编号
def clear_line_text(st_id, r_num):
    s_data=CMD_CLEAR_LINE_TXT+'\t'+str(st_id)+'\t'+str(r_num)
    __infoSendToServer(s_data)
    return

#设置显示方式,速度,停留时间
#参数：st_id 公交站编号，type 显示方式,speed 速度,stop 停留时间
def set_speed(st_id, type, speed, stop):
    s_data=CMD_SET_SPEED+'\t'+str(st_id)+'\t'+str(type)+'\t'+str(speed)+'\t'+str(stop)
    __infoSendToServer(s_data)
    return

#清除屏幕
#参数：st_id 公交站编号
def clear_all(st_id):
    s_data=CMD_CLEAR_ALL+'\t'+str(st_id)
    __infoSendToServer(s_data)
    return

if __name__=='__main__':
    print('test')
    set_total_road(1, 4)
    set_line_text(1, 1, '104', '通畅 3站', '正常 5站')
    clear_line_text(1, 1)
    set_speed(1, 1, 5, 25)
