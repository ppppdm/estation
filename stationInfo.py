# -*- coding: gbk -*-
'''
station.py 公交站信息列表

公交站信息列表
    包含所有的公交站,每个公交站包含了该站应有的线路
    线路信息通过busCalculate.py计算获得.
    
'''


'''
公交站信息
'''
class stopInfo:
    def __init__(self, id, name, lines):
        self.id=id
        self.name=name
        self.lines=lines
        self.info=[None]*len(self.lines)
        return
    
    def getId(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def getLines(self):
        return self.lines

'''
公交车到站信息
    到站信息基本要求要有到站的站数,距离,运行情况,具体的是:
    1.第一个到该站的公交车距离的站数
    2.第二个到该站的公交车距离的站数
    3.第一个到该站的公交车运行情况
    4.第二个到该站的公交车运行情况
    5.该线路到该站是否异常
    6.异常情况发送的信息
    其他根据需求增加
'''
class busToStopInfo():
    def __init__(self):
        self.fisrtNum=0
        self.secondNum=0
        self.firstStatus='正常'
        self.secondStatus='正常'
        self.isUnusual=0
        self.unusualInfo=' '
        return
