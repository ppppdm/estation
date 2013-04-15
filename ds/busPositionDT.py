#  -*- coding: gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
#
#   busPositionDT.py
#   This file define the class busPositionDT.
# The class busPositionDT store the bus position after calculated.
# And user can get all buses position of one bus line from busPositionDT
# by use bus line name.
#
#   We have two designs for the data struct of busPositionDT. One is that
# the busPositionDT just have a list that contains all the busPostionUnit.
# The other is the busPositionDT contains all the bus line, and each line 
# have a list to contain its own busPositionUnit.
#
#   We choose the first as it's simple.
#
#   Though that the busPositionDT is for multi-thread, we should think about
# the sync problem :
#   1.query and insert data at the same time have no sync problem;
#   2.update and insert data at the same time have no sync problem;
#   3.two insert at the same time have sync problem;
#   4.it could not happen that two update at one busPositionUnit at the same
# time;
#
#   Care: Though two update at one busPosittionUnit at the same time could 
# hanppen, we still sync when update one busPositionUnit. This is for safe.
#
# And also define the class busPositionUnit.
# The class have three members:
# bus_id, line_name, bus_pos

import threading

# We define busPositionDT to be a sub class of list
class busPositionDT(list):
    lock = threading.Lock()
    def printDT(self):
        for unit in self:
            unit.printUnit()

    
    # insert a bus position after calculated
    def updateBusPosition(self, bus_id, line_name, bus_pos):
        #busPositionDT.lock.acquire()
        # if had the bus just update position
        for unit in self:
            if unit.bus_id == bus_id:
                unit.setNewPos(line_name, bus_pos)
                print('search found')
                return
        # if not had the bus insert one
        new_u = busPositionUnit(bus_id, line_name, bus_pos)
        # need sync
        busPositionDT.lock.acquire()
        self.append(new_u)
        busPositionDT.lock.release()
        return
    
    # return a list of bus position with the line_name
    def getOneLineBusPos(self, line_name):
        pos_l = list()
        for unit in self:
            if unit.line_name == line_name:
                pos_l.append(unit.bus_pos)
        return pos_l
    
    # for judge whether the bus calculated
    def isHaveBus(self, bus_id):
        for unit in self:
            if unit.bus_id == bus_id:
                return True
        return False
    
    # Use this function should use isHaveBus before
    def insertNewBus(self, bus_id, line_name, bus_pos):
        new_u = busPositionUnit(bus_id, line_name, bus_pos)
        # need sync
        busPositionDT.lock.acquire()
        self.append(new_u)
        busPositionDT.lock.release()
        return
    
    # get one bus by bus_id
    def getBus(self, bus_id):
        for unit in self:
            if unit.bus_id == bus_id:
                return unit
        return None
    
    # delete bus by bus id, if delete return true, else return false
    def deleteBus(self, bus_id):
        for unit in self:
            if unit.bus_id == bus_id:
                self.remove(unit)
                return True
        return False

#
class busPositionUnit:
    def __init__(self, bus_id, line_name, bus_pos):
        self.bus_id = bus_id
        self.line_name = line_name
        self.bus_pos = bus_pos
        self.lock = threading.Lock()
    
    def setNewPos(self, line_name, bus_pos):
        # need sync
        self.lock.acquire()
        self.line_name = line_name
        self.bus_pos = bus_pos
        self.lock.release()
        return
    
    def printUnit(self):
        print(self.bus_id, self.line_name, self.bus_pos)



# for test
if __name__=='__main__':
    # test busPositionDT functions
    bus_position_dt = busPositionDT()
    #bus_position_dt.print()
    

    bus_position_dt.updateBusPosition(7701, ('1', '上行'), 1)
    bus_position_dt.updateBusPosition(7702, ('1', '上行'), 2)
    bus_position_dt.updateBusPosition(7703, ('1', '上行'), 3)
    
    bus_position_dt.printDT()
    
    # test get
    print(bus_position_dt.getOneLineBusPos(('1', '上行')))
    
    # test busPositionUnit
    bus_pos_unit = busPositionUnit(7701, '1', 1)
    bus_pos_unit.printUnit()
    
    # test isHave insertNew delete
    print('have bus 7702', bus_position_dt.isHaveBus(7702))
    print('have bus 7704', bus_position_dt.isHaveBus(7704))
    
    bus_position_dt.insertNewBus(7704, ('2', '下行'), 5)
    
    print('delet bus 7706', bus_position_dt.deleteBus(7706))
    print('delet bus 7704', bus_position_dt.deleteBus(7704))
    
    '''
    # multi thread to busPositionDT
    import time
    import sys
    class MyThread(threading.Thread):
        def __init__(self, i):
            threading.Thread.__init__(self)
            self.i = i
        
        def run(self):
            print(self.i)
            sys.stdout.flush()
            time.sleep(0)
            bus_position_dt.updateBusPosition(self.i, str(self.i), self.i)
            print(self.name + ' update ' + str(len(bus_position_dt)))
            sys.stdout.flush()
            
    for i in range(5):
        t = MyThread(i)
        t.start()
    
    time.sleep(6)
    print('test multi over')
    bus_position_dt.print()
    '''
