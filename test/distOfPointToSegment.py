# -*- coding: gbk -*-
from math import sqrt
from distOfPointToPoint import distOfPointToPoint

#计算点C到线段AB的距离,点A,B,C中的值都是经纬度
def distOfPointToLineSegment(pA, pB, pC):
    #由于计算的点距离都很近,所以将3个点看成一个平面上
    dist=0
    a=distOfPointToPoint(pA, pB)
    b=distOfPointToPoint(pC, pB)
    c=distOfPointToPoint(pA, pC)
    
    if a == 0:
        dist=b
        return dist
    
    #计算点C到直线AB的距离
    ##x=√(2(a^2 b^2+a^2 c^2+b^2 c^2)-(a^4+b^4+c^4))/2a
    tmp=2*(a**2*b**2 + a**2*c**2 + b**2*c**2) - (a**4 + b**4 + c**4)
    if tmp < 0:
        x=0
    else:
        x=sqrt(tmp) / (2 * a)
    #print(x)
    
    #判断过点C作的垂线与直线AB的交点D是否在线段AB上
    #计算线段AD和BD的长度,若AD > AB 或 BD > AB,则交点D在不线段AB上
    ##AD^2+x^2=AC^2
    ##BD^2+x^2=BC^2
    tmp=c**2-x**2
    if tmp < 0:
        AD=0
    else:
        AD=sqrt(tmp)
    tmp=b**2-x**2
    if tmp < 0:
        BD=0
    else:
        BD=sqrt(tmp)
    
    if AD > a or BD > a:
        dist=min((b, c))
    else:
        dist=x
    return dist

############################################################


############################################################
if __name__=='__main__':
    print('test')
