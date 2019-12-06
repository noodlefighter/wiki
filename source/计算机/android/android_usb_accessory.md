

---


参考：
安卓的配件：https://source.android.com/devices/accessories/custom
配件中的AOA模式：https://source.android.com/devices/accessories/protocol

难点主要在device端移植，host端只需要用Libusb操作bulk端点即可。

## device端实现

2. 1. 提取android中的usb_accessory驱动，编译成内核模块
2. 挂上驱动，配置gadgets设备


脚本：
```
	# load kernel module
	modprobe usb_f_accessory

	# 1. Creating the gadgets
	mkdir $CONFIGFS_HOME/usb_gadget/g1
	cd $CONFIGFS_HOME/usb_gadget/g1
	
	echo 0x18D1 > idVendor
	echo 0x2D00 > idProduct
	
	# 2. Creating the configurations
	mkdir configs/c.1
	
	# 3. Creating the functions
	mkdir functions/accessory.usb0
	
	# 4. Associating the functions with their configurations
	ln -s functions/accessory.usb0 configs/c.1
	
	# 5. Enabling the gadget
	# $ echo <udc name> > UDC
	# /sys/class/udc/<udc name>
	UDC_NAME=`ls /sys/class/udc/ | awk "{print $1}"`
	echo $UDC_NAME > UDC
	
	# 6. Set Permission
	chmod 666 /dev/usb_accessory
```

启动后，应用可通过读写/dev/usb_accessory与host通讯了

## 用host端例程来测试

https://github.com/gibsson/linux-adk

device端接收：
```
$ cat /dev/usb_accessory
```

device端发送：
```
$ echo "12345" > /dev/usb_accessory
```

## 速度测试
测试结果：
双向通讯均能超过10Mbyte/s

## 应用tips

* 驱动没实现pull方法，所以select、poll、epoll均无法使用，只能开个线程阻塞读
* 驱动中没有缓存，read时得给根据高速/全速设备，给512/128bytes的缓冲区来读，否则可能漏收、阻塞着不返回
