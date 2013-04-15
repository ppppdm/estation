# -*- coding: gbk -*-

# ������GPS���ݳ���
BUS_DATA_LEN=31

#������GPS���ݰ�ͷ
BUS_DATA_HEAD=0x55

#������GPS���ݰ�β
BUS_DATA_END=0xaa

#������GPS���ݲ���ʹ�õı��
USE_DATA='ud'
NO_HEAD='nh'
NO_END='ne'
LEN_ERR='le'
CHK_ERR='ce'


#infoSending ����ı��
CMD_SET_TOTAL_ROAD='1'
CMD_SET_LINE_TXT='2'
CMD_SET_SPEED='3'
CMD_CLEAR_LINE_TXT='4'
CMD_CLEAR_ALL='5'


#���͸�����վ�Ƶ�������
CODE_TEXT           =0xC1
CODE_VOICE          =0xC2
CODE_CLEAR_TEXT =0xC3
CODE_CLEAR_VOICE=0xC4
CODE_HEART	       =0xC5
CODE_LINE		       =0xC6
CODE_SPEED          =0xC7
CODE_CHECK          =0xC8
CODE_TIME		       =0xC9
CODE_PERH	           =0xCA
CODE_TEMP	       =0xCB
CODE_CLEAR          =0xCC
CODE_PERH1	       =0xCD

CODE_FRAME_HEAD =0xF1
CODE_FRAME_END   =0xAA

LEN_OF_CODE_LINE=0x1
LEN_OF_CODE_CLEAR_TEXT=0x1
LEN_OF_CODE_SPEED=0x3
LEN_OF_CODE_CLEAR=0x0

from lineDistance import lineDistTable
from lineDistance import linesTable
from ds.busPositionDT import busPositionDT

linedist = lineDistTable()
lines = linesTable()
bus_pos_dt = busPositionDT()

# init line data struct
lines.read_from_file('lines.txt')
linedist.read_from_file('linedist.txt')

# init logging
import logging
LOG_FILE   = 'log.txt'
LOG_LEVEL  = logging.DEBUG
LOG_FORMAT = "%(created)-15s %(msecs)d %(levelname)8s %(thread)d %(name)s %(message)s"
logging.basicConfig(filename = LOG_FILE, 
                    level    = LOG_LEVEL, 
                    format   = LOG_FORMAT)

log = logging.getLogger(__name__)

# init 


