---



## 蓝牙协议

GAP 控制蓝牙的广播、连接

GATT 通用属性协议：服务端能通知、广播；客户端能读、写特征值；还定义了“服务”的概念

ATT 属性协议：一项属性包括UUID/Handle/Value，UUID表示“它是什么”，Handle只是属性在设备实现上的序号，Value就是对应的值

## BLE 配对

> refer: 
>
> - [低功耗蓝牙(BLE)配对和解绑](https://blog.csdn.net/sea_snow/article/details/107245400)
> - [esp32例子gatt_security_server](https://github.com/espressif/esp-idf/blob/master/examples/bluetooth/bluedroid/ble/gatt_security_server/tutorial/Gatt_Security_Server_Example_Walkthrough.md)
> - [esp32例子gatt_security_client](https://github.com/espressif/esp-idf/blob/master/examples/bluetooth/bluedroid/ble/gatt_security_client/tutorial/Gatt_Security_Client_Example_Walkthrough.md) 

bonding：生成 LTK (long-term key)，方便下次不用再重新paring

paring：包括“配对能力交换”、“设备认证”、“密钥生成”、“加密连接”等

