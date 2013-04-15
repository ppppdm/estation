# -*- coding:gbk -*-
# auther : pdm
# email  : ppppdm@gmail.com
#
# This file define a function for calculate bus position by bus GPS info.
# After calculated, write the reuslt to busPositionDT

import os
import sys
parent_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_path)

import globalValues
import busCalculate


def calculateBusPosition(busGPSInfo):
    # get line name
    line_name = busGPSInfo.getLineName()
    # get line from linedistTable by line name
    bias = globalValues.lines.getIndexByFullName(line_name)
    line = globalValues.linedist.index(bias)
    pos = busCalculate.busPositionCalculate(line, busGPSInfo)
    globalValues.log.debug(pos)
    
    # write pos to busPositionDT
    globalValues.bus_pos_dt.updateBusPosition(busGPSInfo.id, busGPSInfo.lineName, pos)
    return
