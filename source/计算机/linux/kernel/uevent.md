

---



busybox上的mdev就是用uevent方式实现的hotplug, 而udev上用的是Netlink方式.

```bash
# cat /etc/init.d/S10mdev 

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

uevent编写参考:

 <https://www.cnblogs.com/fastwave2004/articles/4320725.html>

<https://blog.csdn.net/W1107101310/article/details/80211885>

