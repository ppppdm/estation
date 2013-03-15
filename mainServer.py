# -*- coding: gbk -*-
'''
服务主程序
    数据准备：
    1.心跳连接池
    对外服务：
    1.公交车GPS数据接口服务
    2.站牌心跳接收服务
    3.用户控制服务
'''
from connectPool import connectPool
from busCalculate import busCalculate
from net.busDataServer  import busDataServer
from heartBeatServer import heartBeatServer
from infoSendingServer import infoSendingServer

from globalValues import bus_pos_dt


def init():
    bus_pos_dt
    
    
    #bus_pos_dt.insertNewBus(7704, ('2', '下行'), 5)
    bus_pos_dt.print()
    return

from globalValues import initalGlobalValues
initalGlobalValues()


def mainServer():
    
    pool=connectPool()
    
    #_thread.start_new_thread(busDataServe, (0, ))
    #_thread.start_new_thread(reciveHeartBeat, (pool, ))
    #_thread.start_new_thread(netConfigServer, (pool, ))
    
    busdataserver=busDataServer(busCalculate.calculateBusPosition)
    busdataserver.start()
    
    heartbeatserver=heartBeatServer(pool)
    heartbeatserver.start()
    
    infosendingserver=infoSendingServer(pool)
    infosendingserver.start()
    return


if __name__=='__main__':
    init()
    #mainServer()
