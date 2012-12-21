# -*- coding: gbk -*-
'''
路径转换
读取origin_paths文件夹下的原始路径文件并形成用于计算的路径文件写入到paths文件夹内
读取文件格式：
1.51
2.google地图数据
3.宿迁GPS数据
4.百度数据(不用转换)

输出格式：
经度'\t'纬度

命令格式

convPath [51|google|sq|baidu]
'''

import os
import sys

INPUT_DIR='E:\work\estation\origin_paths'
OUTPUT_DIR='E:\work\estation\paths'



def handleError():
    print('cmd arg error')
    print('usage:convPath [51|google|sq]')
    exit()
    return

def handle51File(filename):
    file=open(filename, 'r')
    lines=[]
    while True:
        line=file.readline()
        line=line.strip('\n')
        if line=='':
            break
        arr=line.split('\t')
        arr[0]=arr[0][:3]+'.'+arr[0][3:]
        arr[1]=arr[1][:2]+'.'+arr[1][2:]
        print(arr)
        lines.append(arr)
    file.close()
    return lines

def handleGoogleFile(filename):
    file=open(filename, 'r')
    lines=[]
    while True:
        line=file.readline()
        line=line.strip('\n')
        if line=='':
            break
        arr=line.split('\t')
        arr=(arr[1], arr[0])
        print(arr)
        lines.append(arr)
    file.close()
    return lines

def handleSQFile(filename):
    ##
    return

FUNC_LIST=[handle51File, handleGoogleFile]

def getArgument(args):
    print(args)
    if len(args) <=1:
        handleError()
    
    form=args[1]
    if form=='51':
        return 0
    elif form=='google':
        return 1
    elif form=='sq':
        return 2
    else:
        handleError()

def writePath(lines, filename):
    file=open(filename, 'w')
    s=''
    for i in lines:
        s+=i[0]+'\t'+i[1]+'\n'
    file.write(s)
    file.close()
    return

def delaPaths(dofunc):
    files=os.listdir(INPUT_DIR)
    for i in files:
        print(i)
        lines=dofunc(INPUT_DIR+'\\'+i)
        writePath(lines, OUTPUT_DIR+'\\'+i)
    return

if __name__=='__main__':
    ret=getArgument(sys.argv)
    dofunc=FUNC_LIST[ret]
    delaPaths(dofunc)
    
    print('Done Exit')
