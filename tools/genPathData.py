# -*- coding: gbk -*-
'''
读取lines 和 path 文件夹内的文件生成
lines.txt linepath.txt linestop.txt
'''

import os

LINE_FILE='..\lines.txt'
LINEPATH_FILE='..\linepath.txt'
LINESTOP_FILE='..\linestop.txt'

LINES_DIR='..\..\lines'
PATHS_DIR='..\..\paths'

def handleSQFileOneLine(arr):
    s=''
    name=arr[2]
    lng=str(int(arr[5])/600000)
    lat=str(int(arr[6])/600000)
    s=name+'\t'+lng[:9]+'\t'+lat[:8]
    return s

def handlePathFileOneLine(arr):
    s=arr[0]+'\t'+arr[1]
    return s

def getTasksList():
    tasks_l, lines_l, paths_l=[], [], []
    lines_l=os.listdir(LINES_DIR)
    paths_l=os.listdir(PATHS_DIR)
    print('lines:', lines_l)
    print('paths:', paths_l)
    
    for i in lines_l:
        if i in paths_l:
            tasks_l.append(i)
    print('tasks:', tasks_l)
    return tasks_l

def writeLines(tasks_l):
    file=open(LINE_FILE, 'w')
    s=''
    for i in tasks_l:
        No=i[:-4]
        s+=No+'\t'+'上行'+'\n'+No+'\t'+'下行'+'\n'
    print(s)
    file.write(s)
    file.close()
    return

def writeLineStop(tasks_l):
    file=open(LINESTOP_FILE, 'w')
    s =''
    for i in tasks_l:
        infile=open(LINES_DIR+'\\'+i, 'r')
        infile.readline()
        up, down='', ''
        while True:
            ss=infile.readline()
            ss=ss.strip('\n')
            if ss=='':
                break
            arr=ss.split('\t')
            if arr[3]=='上行':
                up+=handleSQFileOneLine(arr)+'\t'
            else:
                down+=handleSQFileOneLine(arr)+'\t'
        up=up.strip('\t')
        down=down.strip('\t')
        s+=up+'\n'+down+'\n'
        infile.close()
    file.write(s)
    file.close()
    return

def writeLinePath(tasks_l):
    file=open(LINEPATH_FILE, 'w')
    s=''
    for i in tasks_l:
        infile=open(PATHS_DIR+'\\'+i, 'r')
        up, down='', ''
        while True:
            ss=infile.readline()
            ss=ss.strip('\n')
            if ss=='':
                break
            arr=ss.split('\t')
            coor=handlePathFileOneLine(arr)
            up+=coor+'\t'
            down=coor+'\t'+down
        up=up.strip('\t')
        down=down.strip('\t')
        s+=up+'\n'+down+'\n'
        infile.close()
    file.write(s)
    file.close()
    return

if __name__=='__main__':
    tasks=getTasksList()
    writeLines(tasks)
    writeLineStop(tasks)
    writeLinePath(tasks)
    print('Done')
    
    '''
    # test for newline in diff codecs
    import codecs
    f = codecs.open(LINEPATH_FILE, 'r', 'gb2312')
    #f = open(LINEPATH_FILE, 'r',)
    ss = f.readline()
    # for win sys strip('\r\n')
    arr = ss.strip('\r\n').split('\t')
    print(arr)
    '''
