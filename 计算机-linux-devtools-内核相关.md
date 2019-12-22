title: 内核相关
date: 2019-09-23
categories:
- 计算机
- linux
- devtools


---

## 内核中可配置的项目

`/sys/kernel`目录下是所以内核中可配置的项目



## 内核编译时仅编译部分内核模块



```
make modules SUBDIRS=drivers/usb/gadget
```

目录外编译Makefile：

```
LINUX_ROOT   ?= /lib/modules/$(shell uname -r)/build

obj-m        := f_accessory.o

default:
	@make -C $(LINUX_ROOT) M=$(PWD) modules

clean:
	@make -C $(LINUX_ROOT) M=$(PWD) clean
```





