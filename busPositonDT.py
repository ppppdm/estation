#  -*- conding: gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

#   busPositionDT.py
#   This file define the class busPostionDT.
# The class busPositionDT store the bus position after calculated.
# And user can get all buses position of one bus line from busPositionDT
# by use bus line name.
#
#   We have two designs for the data struct of busPositionDT. One is that
# the busPostionDT just have a list that contains all the busPostionUnit.
# The other is the busPostionDT contains all the bus line, and each line 
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

# And also define the class busPositionUnit.
# The class have three members:
# bus_id, line_name, bus_pos

import threading

# We define busPostionDT to be a sub class of list
class busPostionDT(list):
    lock = threading.Lock()
    def print(self):
        for unit in self:
            unit.print()

    
    # insert a bus position after calculated
    def updateBusPosition(self, bus_id, line_name, bus_pos):
        #busPostionDT.lock.acquire()
        # if had the bus just update position
        for unit in self:
            if unit.bus_id == bus_id:
                unit.setNewPos(line_name, bus_pos)
                print('search found')
                return
        # if not had the bus insert one
        new_u = busPositionUnit(bus_id, line_name, bus_pos)
        # need sync
        busPostionDT.lock.acquire()
        self.append(new_u)
        busPostionDT.lock.release()
        return
    
    # return a list of bus position with the line_name
    def getOneLineBusPos(self, line_name):
        pos_l = list()
        for unit in self:
            if unit.line_name == line_name:
                pos_l.append(unit.bus_pos)
        return pos_l

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
    
    def print(self):
        print(self.bus_id, self.line_name, self.bus_pos)



# for test
if __name__=='__main__':
    # test busPostionDT functions
    bus_position_dt = busPostionDT()
    #bus_position_dt.print()
    
    # test update
    bus_position_dt.updateBusPosition(7701, '1', 1)
    bus_position_dt.updateBusPosition(7702, '1', 2)
    bus_position_dt.updateBusPosition(7703, '1', 3)
    '''
    bus_position_dt.print()
    
    # test get
    print(bus_position_dt.getOneLineBusPos('1'))
    
    # test busPositionUnit
    bus_pos_unit = busPositionUnit(7701, '1', 1)
    bus_pos_unit.print()
    '''
    # multi thread to busPostionDT
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
