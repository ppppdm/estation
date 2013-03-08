# -*- coding: gbk -*-
'''
# auther : pdm
# email : ppppdm@gmail.com
# 
# test_busDataClient.py
# 
'''
import sys
sys.path.append("..")
from net import busDataClient


#################TEST####################
from globalValues import USE_DATA
from globalValues import NO_HEAD
from globalValues import NO_END
from globalValues import LEN_ERR
from globalValues import CHK_ERR

TEST_FILE='busGPS_test.txt'

def switchByArg(arr):
    arg=arr[0]
    b_data=b''
    if arg==USE_DATA:
        print(USE_DATA)
        b_data=busDataClient.constructData(arr[1], arr[2], arr[3], arr[4], arr[5])
        busDataClient.sendDataTCP(b_data)
    elif arg== NO_HEAD:
        print(NO_HEAD)
        b_data=busDataClient.constructData(arr[1], arr[2], arr[3], arr[4], arr[5])
        b_data[0]=0
        busDataClient.sendDataTCP(b_data)
    elif arg==NO_END:
        print(NO_END)
        b_data=busDataClient.constructData(arr[1], arr[2], arr[3], arr[4], arr[5])
        b_data[-1]=0
        busDataClient.sendDataTCP(b_data)
    elif arg==LEN_ERR:
        print(LEN_ERR)
        b_data=busDataClient.constructData(arr[1], arr[2], arr[3], arr[4], arr[5])
        b_data+=b'x'
        busDataClient.sendDataTCP(b_data)
    elif arg==CHK_ERR:
        print(CHK_ERR)
        b_data=busDataClient.constructData(arr[1], arr[2], arr[3], arr[4], arr[5])
        b_data[-2]^=1
        busDataClient.sendDataTCP(b_data)
    return

def readTestFile():
    '''从文件中读取测试数据并构造要发送的数据'''
    file =open(TEST_FILE, 'r')
    while True:
        ss=file.readline()
        ss=ss.strip('\n')
        if ss=='':
            break
        arr=ss.split('\t')
        switchByArg(arr)
    file.close()
    return
#########################################

if __name__=='__main__':
    readTestFile()
