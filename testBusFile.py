'''
读取busone.txt文件中的bus信息用于测试

'''

class bus:
    def __init__(self):
        self.path=[]
    
    def readFromFile(self, filename):
        file=open(filename, 'r')
        while True:
            line=file.readline()
            line=line.strip('\n')
            if line=='':
                break
            else:
                arr=line.split(',')
                self.path.append(arr)
        file.close()
        return
    
    def writeTofile(self, filename):
        file=open(filename, 'w')
        s=''
        for i in self.path:
            s+=i[0]+','+i[1]+'\n'
        file.write(s)
        file.close()
        return

if __name__=='__main__':
    print('test')
    bus1=bus()
    bus1.readFromFile('busone.txt')
    bus1.writeTofile('tmp3.txt')
    
    print('exit')
