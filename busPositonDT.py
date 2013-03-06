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

class busPostionDT:
    def __init__(self):
        self.list = list()
    
    def print(self):
        print(self.list)
    
    def updateBusPosition(self):
        return
    
    def getOneLineBus(self):
        return
    
    def getOneLineBusSorted(self):
        return


# for test
if __name__=='__main__':
    bus_position_dt = busPostionDT()
    bus_position_dt.print()
    
