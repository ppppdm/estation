# -*- coding: gbk -*-
'''
# auther : pdm
# email : ppppdm@gmail.com
#
# test_busDataServer.py
#   call busDataServer and wait for client connect.
# also need test_busDataClient run together.
'''

import os
import sys
parent_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_path)
from net import busDataServer

import logging
logging.basicConfig(level=logging.DEBUG, format="%(created)-15s %(msecs)d %(levelname)8s %(thread)d %(name)s %(message)s")
logHandle                = logging.FileHandler('log.txt')
log                      = logging.getLogger(__name__)
log.addHandler(logHandle)

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

def logRet(businfo):
    s=businfo.id+'\t'+str(businfo.lineName)+'\t'+str(businfo.lng)+'\t'+str(businfo.lat)
    log.debug(s)
    return

###########################################

if __name__=='__main__':
    # simple test
    '''
    busdataserver=busDataServer.busDataServer(printRet)
    busdataserver.start()
    '''
    
    # test with busPosition calculate
    import busCalculate
    bc = busCalculate.busCalculate()
    #busdataserver=busDataServer.busDataServer(bc.calculateBusPosition)
    #busdataserver=busDataServer.busDataServer(logRet)
    import test_calculateBusPosition
    busdataserver=busDataServer.busDataServer(test_calculateBusPosition.calculateBusPosition)
    
    busdataserver.start()
