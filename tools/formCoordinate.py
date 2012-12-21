# -*- coding: gbk -*-
'''
读取的形式可以是
1.公交公司提供的公交站文件，lines文件夹下
2.51地图数据，paths文件夹下

转换坐标的格式可以是
1.经度,维度
2.new BMap.Point(经度,维度)


命令格式为

formCoordinate -i [sq|51] -f filename -t [formate]

formate的格式是 *lng*lat*
例如：
    -t lng,lat
    -t new BMap.Point(lng,lat)
'''


def handleError():
    print('cmd arg error')
    print('usage:formCoordinate -i [sq|51] -f filename -t [formate]')
    print('-i    : input data file form')
    print('-f    : input data file name')
    print('-t    : output formate, should be formate like this *lng*lat*,')
    print('        this option should at last')
    print('example:')
    print('formCoordinate -i sq -f ../lines/303.txt -t new BMap.Point(lng,lat)')
    exit()
    return

def handle51file(file):
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
    return lines

def handleSQfile(file):
    lines=[]
    file.readline()
    while True:
        line=file.readline()
        line=line.strip('\n')
        if line=='':
            break
        arr=line.split('\t')
        lng=str(int(arr[5])/600000)

        lat=str(int(arr[6])/600000)
        arr=(lng[:9], lat[:8])
        print(arr)
        lines.append(arr)
    return lines


HANDLE_FUNC=[handleError, handle51file, handleSQfile]



def judge_i_arg(arg):
    if arg=='51':
        return 1
    elif arg=='sq':
        return 2
    else:
        return 0

def judge_f_arg(arg):
    return arg

def getArgument(args):
    index=0
    if '-i' not in args:
        handleError()
    if '-f' not in args:
        handleError()
    
    index=args.index('-i')
    inform=judge_i_arg(args[index+1])
    
    index=args.index('-f')
    filename=judge_f_arg(args[index+1])
    
    pre=mid=pro=''
    if '-t' in args:
        index=args.index('-t')
        s=''
        for i in range(index+1, len(args)):
            s+=args[i]+' '
        print('format=', s)
        if 'lng' not in s or 'lat' not in s:
            print('No have lng lat ')
            handleError()
        midindex=s.index('lng')
        proindex=s.index('lat')
        if midindex > proindex:
            print('lng should left at lat')
            handleError()
        
        print(midindex, proindex)
        pre=s[:midindex]
        mid=s[midindex+3:proindex]
        pro=s[proindex+3:]
        print(pre, '*', mid, '*', pro)
        
    return (inform, filename, (pre, mid, pro))

def write_to_file(lines, form):
    file=open('tmp.txt', 'w')
    s=''
    for i in lines:
        s+=form[0]+i[0]+form[1]+i[1]+form[2]+'\n'
    file.write(s)
    print(s)
    file.close()
    print('output write to tmp.txt')
    return


def dealFile(filename, form, funcIndex):
    file=open(filename, 'r')
    dofunc=HANDLE_FUNC[funcIndex]
    lines=dofunc(file)
    write_to_file(lines, form)
    
    file.close()
    return


if __name__=='__main__':
    import sys
    print(sys.argv)
    ret=getArgument(sys.argv)
    dealFile(ret[1], ret[2], ret[0])
    print('Done Exit')


