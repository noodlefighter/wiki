

---



## 从hotplug说起

busybox上的mdev是用sysfs写入需要触发时执行的程序的方式实现的hotplug.

这是mdev的启动脚本`/etc/init.d/S10mdev `, 开机时给hotplug内核模块传入自身路径.

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

而udev上实现hotplug用的是uevent方式.



> TODO:

uevent编写参考:

 <https://www.cnblogs.com/fastwave2004/articles/4320725.html>

<https://blog.csdn.net/W1107101310/article/details/80211885>

