# -*- coding: gbk -*-
'''
本模块维护电子站牌IP地址表.
电子站牌的IP地址表由table_IP.py定义.

维护电子站牌IP地址表包括:
1.修改对应编号的站牌的IP地址

以上操作将调用table_IP提供的操作.

修改电子站牌的IP地址,维护模块通过多线程的方式.
每次操作建立独立的线程操作IP地址表.

维护模块在整个电子站牌服务启动时启动.
启动时绑定一个电子站牌IP地址表.
'''


import _thread


class maintainIP:
    def __init__(self,  ip_table):
        self.ip_table=ip_table
    '''
    restoreIP函数将启动一个新线程,调用内部函数_restoreIP处理数据
    '''
    def restoreIP(self, num, ip):
        _thread.start_new_thread(self._restoreIP, (num, ip))
        return
    
    def _restoreIP(self, num, ip):
        self.ip_table.setIP(num, ip)
        '''
        在测试的时候每次添加ip将把ip table写入到文件中
        非测试时将写入文件注释
        '''
        self.ip_table.writeToFile()
        return


if __name__=='__main__':
    from table_IP import table_IP
    def test():
        iptable=table_IP()
        mip=maintainIP(iptable)
        for i in range(10):
            mip.restoreIP(i,  '127.0.0.1')
        return
    test()
