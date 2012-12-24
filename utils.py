# -*- coding: gbk -*-

'''
crc 校验和，参数是bytesArray，返回校验和(各位异或)
'''

def crc_check(b_data):
    if len(b_data)==0:
        return 0
    crc=b_data[0]
    for i in b_data[1:]:
        crc^=i
    return crc
