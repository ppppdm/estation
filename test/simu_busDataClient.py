# -*- coding: gbk -*-
'''
# auther : pdm
# email : ppppdm@gmail.com
#
# simu_busDataClient.py
#   Simulate busDataClient. send bus data by busDataClient.py.
# And watch the estation system whether work well.
'''

import sys
sys.path.append('..')

from net import busDataClient


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


if __name__=='__main__':
    simu_busDataClient()
