## BlueZ接入蓝牙HCI

接入蓝牙：

```
# btattach -B /dev/ttyUSB2 -P h4 -S 921600
```

启动：

```
# hciconfig
hci1:	Type: Primary  Bus: UART
	BD Address: 8C:AA:B5:94:7F:9E  ACL MTU: 1021:9  SCO MTU: 255:4
	UP RUNNING
	RX bytes:755 acl:0 sco:0 events:47 errors:0
	TX bytes:1039 acl:0 sco:0 commands:47 errors:0

hci0:	Type: Primary  Bus: USB
	BD Address: D4:D2:52:5B:8A:D7  ACL MTU: 1021:4  SCO MTU: 96:6
	UP RUNNING
	RX bytes:3566 acl:0 sco:0 events:237 errors:0
	TX bytes:3609 acl:0 sco:0 commands:237 errors:0

# hciconfig hci1 up
```

测试：

```
# hcitool dev
Devices:
	hci1	8C:AA:B5:94:7F:9E
	hci0	D4:D2:52:5B:8A:D7
# hcitool -i hci1 lescan
```

