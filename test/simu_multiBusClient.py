# -*- coding: gbk -*-
'''
# auther : pdm
# email : ppppdm@gmail.com
#
# simu_multiBusClient.py
# This file simulation multi bus gps data send to server.
# Three's some params can set to this simulation
# -n ---- the simulate bus number
# -m ---- interval time(sec) bus send gps data
# -f ---- bus gps data file
# command may like this
# multiBusClient.py -n 10 -m 5 -f busone.txt
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


import coor_2_gps


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
        #print(pos)
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
        print(self.ident, self.getName())
        # first read bus gps data file(ro)
        try:
            file = open(BUS_GPS_FILE, 'r')
            gps_datas = getFileData(file)
            file.close()
        
            # second send data
        
            for pos in gps_datas:
                lng = coor_2_gps.coordinate2GPS(pos[0])
                lat = coor_2_gps.coordinate2GPS(pos[1])
                data = busDataClient.constructData(self.bus_id, self.line, self.stream, lng, lat)
                busDataClient.sendDataTCP(data)
                time.sleep(self.interval_time)
            ''''''
        except Exception as e:
            print(e)
            print(self.getName, 'exit!')
        return

def exit_nicely():
    exit()

def getArgument(args):
    print('get args', args)
    global INTERVAL_TIME
    global BUS_NUMBER
    global BUS_GPS_FILE
    bias = 0
    while bias < len(args):
        if args[bias] == '-t':
            bias+=1
            if args[bias].isdigit():
                INTERVAL_TIME = int(args[bias])
                bias+=1
            else:
                exit_nicely()
        elif args[bias] == '-n':
            bias+=1
            if args[bias].isdigit():
                BUS_NUMBER = int(args[bias])
                bias+=1
            else:
                exit_nicely()
        elif args[bias] == '-f':
            bias+=1
            BUS_GPS_FILE = args[bias]
            bias+=1
        else:
            bias+=1
    return

if __name__=='__main__':
    print(__file__,'Test begin!')
    print(sys.argv)
    getArgument(sys.argv[1:])
    thread_list = list()
    
    for i in range(BUS_NUMBER):
        
        bus_client = busClient(str(i).zfill(4), '303', '上行', INTERVAL_TIME)
        bus_client.start()
        thread_list.append(bus_client)
        time.sleep(1)
    
    for i in thread_list:
        i.join()
    print('Simu done!')

