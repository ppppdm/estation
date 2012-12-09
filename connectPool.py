# -*- coding: gbk -*-
'''
conncetPool.py 电子站牌连接池表
    GPRS模块处于无线网络的内网中,因此服务器侦听到的连接的IP地址是无线网络路由的IP地址.
服务器是没法主动建立与电子站牌的连接的.
    所以电子站牌服务侦听到连接后需要将连接保持到连接池中,使用时从连接池中取出连接与电子站牌通信.
    因此table_IP.py(将连接的IP地址写到文件中)和maintainIP.py没有用了.
    
数据结构:
    编号 连接
    
功能:
    1.将一对连接加入到连接池中
    2.根据编号从连接池中取出连接

注意:
    调用的上层应该判断该连接是否为可用连接,不可用连接将不再加入连接池中.
    
    显然连接失效只有在连接池中发生,所以返回给上层的连接可能是无效的连接
'''

class connectPool:
    def __init__(self):
        self.pool=dict()
    
    def addConn(self, num, coon):
        self.pool[num]=coon
        return
    
    def getConn(self, num):
        try:
            return self.pool.pop(num)
            #使用pop 将coon移出,以防出错时更新了正在使用的连接
            #虽然按照正常情况使用中的连接不会更新
        except KeyError:
            print('connectPool key error')
            return None
    
    def printPool(self):
        print(self.pool)

CONN_LIST_LENGTH=10000
INIT_CONN=None

class conncetList():
    def __init__(self):
        self.list=[INIT_CONN]*CONN_LIST_LENGTH
        return
    
    def get(self, num):
        print(len(self.list))
        return self.list[num]
    
    def set(self, num, conn):
        self.list[num]=conn
        return

if __name__=='__main__':
    a, b=1, 's'
    pool=connectPool()
    pool.addConn(a, b)
    pool.printPool()
    a, b=2,'c'
    pool.addConn(a,b)
    pool.printPool()
    print(pool.getConn(2))
    print(pool.getConn(3))
    pool.printPool()

    cl=conncetList()
    print(cl.get(0))
    print(cl.set(0, 'x'))
