# -*- coding: gbk -*-
# auther : pdm
# email  : ppppdm@gmail.com
# UerControlInfoTable.py
# UerControlInfoTable store station information that user setting.
# Infomation can be :
#    station_name, line_name, info,
# operation:
#    insert, update, delete, query
# insert(update) one setting;
# delete one setting;
# query setting[all, by station_name, by line_name]

# This table isn't thread safe.

info_list = []

def insert_setting(station_name, line_name, info):
    for i in info_list:
        if i[0] == station_name and i[1]==line_name:
            i[2] = info
            return
    info_list.append([station_name, line_name, info])
    return

def delete_setting(station_name, line_name):
    for i in info_list:
        if i[0] == station_name and i[1]==line_name:
            info_list.remove(i)
            return True
    return False

def query_all():
    return info_list

def query(station_name, line_name):
    for i in info_list:
        if i[0] == station_name and i[1]==line_name:
            return i
    return

if __name__=='__main__':
    print(__file__, 'test')
    
    # test insert
    print('test insert')
    insert_setting('xx', ['303', 'up'], 'a;sfd;a')
    insert_setting('yy', ['303', 'up'], 'a;sfd;a')
    
    print(query_all())
    
    # test update
    print('test update')
    insert_setting('zz', ['303', 'dw'], 'a;sfd;a')
    insert_setting('zz', ['303', 'dw'], 'zzzzzzz')
    
    print(query_all())
    
    # test delete
    print('test delete')
    delete_setting('yy', ['303', 'up'])
    delete_setting('zz', ['303', 'up'])
    
    print(query_all())
    
    # test query
    print('test query')
    print(query('yy', ['303', 'up']))
    print(query('xx', ['303', 'up']))
    print(query('zz', ['303', 'dw']))
    
    
    
    

