---

## u-boot SPL

refer: https://stackoverflow.com/questions/31244862/what-is-the-use-of-spl-secondary-program-loader

当系统内部内存（SRAM）装不下完整的uboot时，这时候需要使用被称为**SPL**的精简代码初始化内存。

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

