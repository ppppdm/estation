estation
========

宿迁 电子站牌后台服务

一.文件列表
	utils.py
	busDataClient.py
	busDataServer.py
	globalValues.py
	network.py

二.文件概述
	utils.py           常用工具，包括crc校验和。
	busDataClient.py   发送公交车GPS数据的客户端，暂时为模拟客户端，读入测试数据文件进行测试。
	busDataServer.py   接收公交车GPS数据的服务端。
	globalValues.py    全局定义的常量
	network.py         网络主机和端口定义
	ds/stationBusInfo.py	由一条线路上所有车辆的位置计算该条线路所有站的最近次近到站站数
	ds/busPosition_V2R.py 将公交车在虚拟线路上的位置转为实际线路所在的位置
	ds/busPositionDT.py 提供将公交车位置储存，更新和取出。类似数据库。
