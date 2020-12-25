# Linux内核编译

## 编译Linux内核如何获取帮助？

- Linux内核的Makefiles说明文档：https://www.kernel.org/doc/Documentation/kbuild/makefiles.txt

- 在内核路径下使用：`make ARCH=arm help`命令

  

## 编译Linux内核速查

```
交叉编译例：
make ARCH=arm CROSS_COMPILE=arm-linux-eabi-

保存经过精简的defconfig例：
make ARCH=arm savedefconfig

安装内核模块到指定路径：
make ARCH=arm modules_install INSTALL_MOD_PATH=xxx_dir/

```



## Linux内核编译时仅编译部分内核模块

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