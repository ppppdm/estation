# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com
# recv user control setting information

import socket
import threading
import network
import globalValues

def process_data(b_data):
    data = str(b_data, 'gbk')
    print(data)
    # just insert None right now
    globalValues.user_info_table.insert(None, None, None)

class userControlInfoServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((network.HOST_OF_USERCONTROL, network.PORT_OF_USERCONTROL))
            sock.listen(5)
            while True:
                conn, addr = sock.accept()
                print('connected by ', addr, conn)
                
                # recv user setting and insert to UserControlInfoTable
                b_data = conn.recv(1024)
                process_data(b_data)
                
                sock.close()
        except Exception as e:
            print(e)


if __name__=='__main__':
    print(__file__, 'test')
