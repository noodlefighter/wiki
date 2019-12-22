title: telnet
date: 2019-10-28
categories:
- 计算机
- linux
- devtools




---



## busybox下开启telnet的方法



在busybox下尝试编译telnetd，无法连接，`telnetd -F`把服务放前台运行，得到错误日志：

```
telnetd: can't find free pty
```

解决方法：

Linux Kernel Config:

```
CONFIG_UNIX98_PTYS=y
```

Busybox Config:

```
CONFIG_FEATURE_DEVPTS=y
```

Rootfs:

```
mkdir /dev/pts
mount -t devpts devpts /dev/pts
mknod -m 666 /dev/ptmx c 5 2
```

