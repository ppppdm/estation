from math import sin
from math import cos
from math import acos
from math import pi

EARTH_RADIUS=6371.004 #单位km
R=EARTH_RADIUS

#计算点A和点B的球面距离,点A,B的值是经纬度
def distOfPointToPoint(pA, pB):
    lngA, latA=float(pA[0])*pi/180, float(pA[1])*pi/180
    lngB, latB=float(pB[0])*pi/180, float(pB[1])*pi/180
    
    #预处理
    #北纬取90-纬度值(90- Latitude)，南纬取90+纬度值(90+Latitude)
    #这里都是北纬,也没有南北纬信息用于处理,以后可能会添加
    
    '''
    ##角C余弦值 = sin(LatA)*sin(LatB) + cos(LatA)*cos(LatB)*cos(MLonA-MLonB)
    '''
    C=sin(latA)*sin(latB)+cos(latA)*cos(latB)*cos(lngA-lngB)
    
    '''
    ##注意:C的值被实际问题和计算精度影响,C的值是否在arcos的定义域取值范围内[-1,1]
    '''
    if C > 1:
        C=1
    if C < -1:
        C=-1
    
    dist=R*acos(C)
    return dist

#####################################################
TEST_FILE='pointToPoint_test.txt'
OUT_FILE='pointToPoint_result.txt'

def readTestFile():
    outfile=open(OUT_FILE, 'w')
    infile=open(TEST_FILE, 'r')
    while True:
        ss=infile.readline()
        ss=ss.strip('\t')
        if ss=='':
            break
        arr=ss.split('\t')
        pA=(arr[0], arr[1])
        pB=(arr[2], arr[3])
        dist=distOfPointToPoint(pA, pB)
        outfile.write(str(dist)+'\n')
    
    infile.close()
    outfile.close()
    return

#####################################################

if __name__=='__main__':
    readTestFile()
    print('test')
