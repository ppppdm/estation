# -*- coding: gbk -*-
'''
# auther : pdm
# email : ppppdm@gmail.com
#
# test_busDataServer.py
#   call busDataServer and wait for client connect.
# also need test_busDataClient run together.
'''

import parentPath
parentPath.impt()
from net import busDataServer

##########################################
FILENAME='busData.txt'
file=None


def write_to_file(businfo):
    try:
        file=open(FILENAME, 'w')
    except IOError:
        print('open file error')
    else:
        print('open file ok')
    s=''
    s+=businfo.id+'\t'+str(businfo.lineName)+'\t'+str(businfo.lng)+'\t'+str(businfo.lat)+'\n'
    file.write(s)
    file.flush()
    file.close()
    return

def printRet(businfo):
    s=businfo.id+'\t'+str(businfo.lineName)+'\t'+str(businfo.lng)+'\t'+str(businfo.lat)
    print(s)
###########################################

if __name__=='__main__':
    busdataserver=busDataServer.busDataServer(printRet)
    busdataserver.start()
