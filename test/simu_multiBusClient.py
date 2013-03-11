# -*- coding: gbk -*-
'''
# auther : pdm
# email : ppppdm@gmail.com
#
# simu_multiBusClient.py
# This file simulation multi bus gps data send to server.
# Three's some params can set to this simulation
# n ---- the simulate bus number
# m ---- interval time(sec) bus send gps data
# 
# command may like this
# multiBusClient.py -n 10 -m 5
# 
# Bus's gps data use a default file that orgnized before.
# 
'''
import threading
import time
import os
import sys
parent_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_path)
from net import busDataClient


BUS_NUMBER = 1
INTERVAL_TIME = 5   # sec
BUS_GPS_FILE = 'busone.txt'

def getFileData(file):
    datas = []
    while True:
        ss = file.readline()
        ss = ss.strip('\n')
        if ss == '':
            break
        pos = ss.split(',')
        print(pos)
        datas.append(pos)
    return datas

class busClient(threading.Thread):
    def __init__(self, bus_id, line, stream, interval_time):
        threading.Thread.__init__(self)
        self.bus_id = bus_id
        self.line = line
        self.stream = stream
        self.interval_time = interval_time
        
    def run(self):
        
        # first read bus gps data file(ro)
        file = open(BUS_GPS_FILE, 'r')
        gps_datas = getFileData(file)
        file.close()
        # second send data
        for pos in gps_datas:
            lng = pos[0]
            lat = pos[1]
            data = busDataClient.constructData(self.bus_id, self.line, self.stream, lng, lat)
            busDataClient.sendDataTCP(data)
            time.sleep(self.interval_time)
        
        return

if __name__=='__main__':
    print(__file__,'Test begin!')
    
    for i in range(BUS_NUMBER):
        
        bus_client = busClient(str(i).zfill(4), '303', '上行', INTERVAL_TIME)
        bus_client.start()
    
    print('Simu done!')

