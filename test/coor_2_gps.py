# -*- coding: gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
#
# coor_2_gps.py



def coordinate2GPS(coordinate):
    return float(coordinate) * 600000

def GPS2coordinate(GPS):
    return float(GPS) / 600000

def formateToStr(gps):
    # the argument gps type is float
    return

if __name__=='__main__':
    print(__file__, 'Test begin!')
    o_coor = '118.216117'
    o_gps = '70922263'
    
    gps = coordinate2GPS(o_coor)
    print(gps)
    
    coor = GPS2coordinate(o_gps)
    print(coor)
