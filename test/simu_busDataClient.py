# -*- coding: gbk -*-
'''
# auther : pdm
# email : ppppdm@gmail.com
#
# simu_busDataClient.py
#   Simulate busDataClient. send bus data by busDataClient.py.
# And watch the estation system whether work well.
'''

import os
import sys
parent_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_path)

from net import busDataClient
import coor_2_gps
import time


def simu_busDataClient():
    bus_id=str(7023)
    line='303'
    stream='上行'
    lng=str(70922263)
    lat=str(20374106)
    
    data=busDataClient.constructData(bus_id, line, stream, lng, lat)
    
    busDataClient.sendDataTCP(data)
    print('exit')
    return

def simu_busDataClientByFile(filename):
    bus_id=str(7023)
    line='303'
    stream='上行'
    try:
        file = open(filename, 'r')
        gps_datas = getFileData(file)
        file.close()
        
            # second send data
        
        for pos in gps_datas:
            lng = coor_2_gps.coordinate2GPS(pos[0])
            lat = coor_2_gps.coordinate2GPS(pos[1])
            data = busDataClient.constructData(bus_id, line, stream, lng, lat)
            busDataClient.sendDataTCP(data)
            time.sleep(1)
            ''''''
    except Exception as e:
            print(e)
    return

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

if __name__=='__main__':
    #simu_busDataClient()
    simu_busDataClientByFile('busone.txt')
