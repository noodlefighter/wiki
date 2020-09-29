

Linux下可以用`/dev/mem`设备直接访问物理地址空间的RAM，当然了得是root权限

---

## memtool Linux直接访问内存工具

最简单的寄存器修改程序，buildroot里有包。

https://public.pengutronix.de/software/memtool/



## devmem Linux直接访问内存工具

busybox自带的内存访问工具，能读写内存地址