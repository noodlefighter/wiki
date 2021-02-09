

## Linux rootfs中的dev目录

> via: http://velep.com/archives/334.html

在嵌入式ARM开发中，用busybox制作根文件系统时，其中必须构建的一个目录就是/dev目录。这个目录对所有的用户都十分重要，因为在这个目录中包含了所有Linux系统中使用到的外部设备，即所有的设备节点。

1. 静态构建：

使用静态方法构建，就是根据预先知道要挂载的驱动，用mknod命令逐一构建各种设备节点。
新建/dev目录，先创建5个设备文件(必须的)：

```
mkdir -p root_fs/dev
cd root_fs/dev
sudo mknod console c 5 1
sudo mknod null c 1 3
sudo mknod ttySAC0 c 204 64
sudo mknod mtdblock0 b 31 0
sudo mknod mtdblock1 b 31 1
sudo mknod mtdblock2 b 31 2
```

其他设备文件：当系统启动后，使用cat /proc/devices命令查看内核中注册了那些设备，然后一一创建相应的设备文件。

使用静态创建dev目录的缺点：不支持热插拔设备。

2. mdev动态创建：

busybox的mdev文档
https://git.busybox.net/busybox/plain/docs/mdev.txt

mdev是udev的简化版本，通过读取内核相应信息来动态创建设备文件或设备节点。其主要用途有：初始化dev目录、动态更新、支持热插拔。要使用mdev设备管理系统，需要内核支持sysfs文件系统，为了减少Flash的读写，还要支持tmpfs文件系统(事实上目前dev目录都为tmpfs文件系统目录)。一般情况下，默认的内核配置已经满足使用mdev的要求。

修改etc/init.d/rcS文件，修改后如下：

```
#!/bin/sh

echo "Mount Pseudo Filesystem ......"
mount -t tmpfs -o size=64k,mode=0755 tmpfs /dev  // dev目录为tmpfs文件系统目录
mkdir /dev/pts
mount -t devpts devpts /dev/pts
mount -t sysfs sysfs /sys
echo /sbin/mdev > /proc/sys/kernel/hotplug   // 支持热插拔
mdev -s
```

其中的语句是和mdev的使用方法几乎一样。可参考busybox/doc/mdev.txt文档。

另外，mdev是通过init进程启动，在使用mdev构造/dev目录前，init进程至少要用到/dev/console和/dev/null，所以要像使用静态方法一样先构建它们。在/dev/下执行

```
sudo mknod console c 5 1
sudo mknod null c 1 3
```


## 自己构建的rootfs，启动内核时提示not found /dev/null

内核需要有devtmpfs特性，`/etc/fstab`中开机挂载dev目录为devtmpfs，问题解决。


## modprobe提示can't change directory to '3.18.20': No such file or directory


发现是执行modprobe时提示的，查看rcS脚本：

```
# cd /etc/init.d/
# ls
S01syslogd  S10mdev     S40network  rcS
S02klogd    S20urandom  rcK
# cat S10mdev
#!/bin/sh
#
# Start mdev....
#

case "$1" in
  start)
        echo "Starting mdev..."
        echo /sbin/mdev >/proc/sys/kernel/hotplug
        /sbin/mdev -s
        # coldplug modules
        find /sys/ -name modalias -print0 | xargs -0 sort -u | tr '\n' '\0' | \
            xargs -0 modprobe -abq
        ;;
  stop)
        ;;
  restart|reload)
        ;;
  *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
esac

exit $?
```

功能是在启动时，如果/sys有包含`modalias`的设备，就尝试用modprobe挂载对应内核模块（.ko文件），需要做的事情:

1. 内核模块放入/lib/module/`uname -r`；
2. 创建modules.dep。


## 修改Linux中dev文件夹中tty的数量

先弄清linux的虚拟终端是做什么用的，这里有篇《Linux Virtual Console (1) : From User's Perspective》的[译文](https://blog.csdn.net/astrotycoon/article/details/79001713)

linux kernel配置中对虚拟终端的描述：

```
CONFIG_VT:                                                      
                                                                
If you say Y here, you will get support for terminal devices with  
display and keyboard devices. These are called "virtual" because you
can run several virtual terminals (also called virtual consoles) on
one physical terminal. This is rather useful, for example one   
virtual terminal can collect system messages and warnings, another 
one can be used for a text-mode user session, and a third could run
an X session, all in parallel. Switching between virtual terminals 
is done with certain key combinations, usually Alt-<function key>. 

The setterm command ("man setterm") can be used to change the   
properties (such as colors or beeping) of a virtual terminal. The  
man page console_codes(4) ("man console_codes") contains the special
character sequences that can be used to change those properties
directly. The fonts used on virtual terminals can be changed with  
the setfont ("man setfont") command and the key bindings are defined
with the loadkeys ("man loadkeys") command.                     
                                                                   
You need at least one virtual terminal device in order to make use  
of your keyboard and monitor. Therefore, only people configuring an 
embedded system would want to say N here in order to save some      
memory; the only way to log into such a system is then via a serial 
or network connection.
                                 
If unsure, say Y, or else you won't be able to do much with your new
shiny Linux system :-)

如果您在这里说Y，您将获得带有显示和键盘设备的终端设备的支持。这些被称为“虚拟”，因为您可以在一个物理终端上运行多个虚拟终端（也称为虚拟控制台）。这是非常有用的，例如，一个虚拟终端可以收集系统消息和警告，另一个可以用于文本模式用户会话，第三个可以并行运行X会话。使用某些组合键完成虚拟终端之间的切换，通常是Alt-<功能键> 

setterm命令可用于更改虚拟终端的属性（如颜色或蜂鸣声）。Theman page console_codes（4）包含可用于直接更改这些属性的特殊字符序列。可以使用setfont命令更改虚拟终端上使用的字体，并使用loadkeys命令定义键绑定。

您需要至少一个虚拟终端设备才能使用键盘和显示器。因此，只有配置嵌入式系统的人才会想在这里说N以节省一些内存;登录这样一个系统的唯一方法就是通过串行或网络连接。

如果不确定，请说Y，否则你将无法在你的新系统上操作。
```

https://askubuntu.com/questions/377213/why-so-many-virtual-consoles
提到改变tty数量的具体方法——修改内核，但是这对新的内核已经不管用了，`include/linux/*.h`已经拆分部分到`include/uapi/linux/*.h`了，应该修改`include/uapi/linux/vt.h`的`MAX_NR_CONSOLES`，但实际追踪了一下代码，减少这个值并不会带来多少收益。

尝试修改一下吧，重启后立即查看内存使用，修改前：
```
# free
             total       used       free     shared    buffers     cached
Mem:         58516       9628      48888         32          0       1332
-/+ buffers/cache:       8296      50220
Swap:            0          0          0
```

修改后：
```
# free
             total       used       free     shared    buffers     cached
Mem:         58516       9304      49212         32          0       1348
-/+ buffers/cache:       7956      50560
Swap:            0          0          0

```
