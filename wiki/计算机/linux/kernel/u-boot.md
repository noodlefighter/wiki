---

## u-boot SPL

refer: https://stackoverflow.com/questions/31244862/what-is-the-use-of-spl-secondary-program-loader

当系统内部内存（SRAM）装不下完整的uboot时（或者ROM Bootloader对启动代码有长度限制），这时候需要使用被称为**SPL**的精简代码初始化内存。

```
+--------+----------------+----------------+----------+
| Boot   | Terminology #1 | Terminology #2 | Actual   |
| stage  |                |                | program  |
| number |                |                | name     |
+--------+----------------+----------------+----------+
| 1      |  Primary       |  -             | ROM code |
|        |  Program       |                |          |
|        |  Loader        |                |          |
|        |                |                |          |
| 2      |  Secondary     |  1st stage     | u-boot   |
|        |  Program       |  bootloader    | SPL      |
|        |  Loader (SPL)  |                |          |
|        |                |                |          |
| 3      |  -             |  2nd stage     | u-boot   |
|        |                |  bootloader    |          |
|        |                |                |          |
| 4      |  -             |  -             | kernel   |
|        |                |                |          |
+--------+----------------+----------------+----------+
```

配置了`CONFIG_SPL`后，会生成`u-boot.bin`和`u-boot-xxx-with-spl.bin`，前者为完整u-boot，后者为带了SPL头部的u-boot。

## u-boot引导linux启动

u-boot用户手册相关章节：

https://www.denx.de/wiki/view/DULG/BootingEmbeddedLinux



1. 把kernel、设备树dtb加载到内存里
2. 设置环境变量bootargs等
3. `bootz/bootm`命令引导





## bootm和bootz命令的区别

bootz对应linux kernel的zImage，裸机二进制文件。

bootm对应linux kernel的uImage，mkimage工具做的warpper的镜象，附带着额外信息，如文件大小、LOADADDR、校验信息等。生成uImage：

```
$ ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- LOADADDR=0x80008000 make uImage
```

或者使用mkimage工具制作：

```
mkimage -A arm -O linux -T kernel -C none -a 0x80008000 -e 0x80008000 -n 'Linux-3.0' -d arch/arm/boot/zImage arch/arm/boot/uImage
```



## boot.scr脚本

可以在启动时加载脚本，实现动态传参，不用重新编译u-boot，一个实例：

```
bootcmd=run findfdt;mmc dev ${mmcdev};mmc dev ${mmcdev}; if mmc rescan; then if run loadbootscript; then run bootscript; else if run loadimage; then run mmcboot; else run netboot; fi; fi; else run netboot; fi
loadbootscript=fatload mmc ${mmcdev}:${mmcpart} ${loadaddr} ${script};
```

sd卡启动，启动时先尝试加载脚本，如果存在则执行loadbootscript

编译boot.scr，需要用到u-boot构建出的mkimage工具：

```
$ mkimage -A arm -T script -O linux -d boot.txt boot.scr
Image Name:
Created:      Tue Apr 19 06:44:13 2022
Image Type:   ARM Linux Script (gzip compressed)
Data Size:    84 Bytes = 0.08 kB = 0.00 MB
Load Address: 00000000
Entry Point:  00000000
Contents:
   Image 0: 76 Bytes = 0.07 kB = 0.00 MB
```





## u-boot使用网口

```
setenv ipaddr 192.168.200.119
setenv ethaddr 11:22:33:44:55:66
setenv netmask 255.255.255.0
setenv gatewayip 192.168.200.1
```



