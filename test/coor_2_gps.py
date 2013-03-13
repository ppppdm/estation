# -*- coding: gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
#
# coor_2_gps.py

GPS_FORMAT_LEN = 8

def coordinate2GPS(coordinate):
    gps = str(float(coordinate) * 600000)
    gps = gps.partition('.')[0]
    if len(gps) < GPS_FORMAT_LEN:
        gps = gps.zfill(GPS_FORMAT_LEN)
    else:
        gps = gps[:GPS_FORMAT_LEN]
    return gps

def GPS2coordinate(GPS):
    return float(GPS) / 600000

def formateToStr(gps):
    # the argument gps type is float
    return

if __name__=='__main__':
    print(__file__, 'Test begin!')
    o_coor = '2.216117'
    o_gps = '70922263'
    
    gps = coordinate2GPS(o_coor)
    print(gps)
    
    
    
    coor = GPS2coordinate(o_gps)
    print(coor)
