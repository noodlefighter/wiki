title: ble蓝牙
date: 2019-07-27
categories:
- 电子工程
- 嵌入式软件


---



## 蓝牙协议

GAP 控制蓝牙的广播、连接

GATT 通用属性协议：服务端能通知、广播；客户端能读、写特征值；还定义了“服务”的概念

ATT 属性协议：一项属性包括UUID/Handle/Value，UUID表示“它是什么”，Handle只是属性在设备实现上的序号，Value就是对应的值

