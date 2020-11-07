

---



## linux的hotplug机制

busybox上的mdev是用sysfs写入需要触发时执行的程序的方式实现的hotplug.

这是mdev的启动脚本`/etc/init.d/S10mdev `, 开机时给内核传入自身路径.

```bash
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
...
```



根据[linux的文档](https://www.kernel.org/doc/html/latest/driver-api/usb/hotplug.html)：

```
Kernel Hotplug Helper (/sbin/hotplug)
There is a kernel parameter: /proc/sys/kernel/hotplug, which normally holds the pathname /sbin/hotplug. That parameter names a program which the kernel may invoke at various times.

The /sbin/hotplug program can be invoked by any subsystem as part of its reaction to a configuration change, from a thread in that subsystem. Only one parameter is required: the name of a subsystem being notified of some kernel event. That name is used as the first key for further event dispatch; any other argument and environment parameters are specified by the subsystem making that invocation.

Hotplug software and other resources is available at:

http://linux-hotplug.sourceforge.net
Mailing list information is also available at that site.
```

可见早些年的linux发行版，使用的是一个叫hotplug的uevent_helper。



> TODO:

uevent编写参考:

 <https://www.cnblogs.com/fastwave2004/articles/4320725.html>

<https://blog.csdn.net/W1107101310/article/details/80211885>

