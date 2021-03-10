

## openwrt编译笔记

用到的仓库：

https://github.com/coolsnowwolf/lede

https://github.com/kenzok8/openwrt-packages



## UCI

文档：https://openwrt.org/docs/guide-user/base-system/uci

UCI是openwrt的配置接口

一个uci配置文件例子`/etc/config/sys`：

```
config app
	option workmode 'rtsp'
```

命令行get/set：

```
$ uci get sys.@app[0].workmode
rtsp
$ uci set sys.@app[0].workmode='uvc'
```



## openwrt的工具

包[block-mount](https://openwrt.org/packages/pkgdata_lede17_1/block-mount)，http://git.openwrt.org/project/fstools.git提供的block工具，和blkid命令差不多：

```
# block info
/dev/loop0: UUID="4d6fe5a0-de0c-4945-9c91-8284225b7295" LABEL="rootfs_data" VERSION="1.13" MOUNT="/overlay" TYPE="f2fs"
/dev/sda1: UUID="84173db5-fa99-e35a-95c6-28613cc79ea9" LABEL="kernel" VERSION="1.0" MOUNT="/boot" TYPE="ext4"
/dev/sda2: UUID="5bdbe408-d6fc5cf7-c1c9f393-d4ff4ca9" VERSION="4.0" MOUNT="/rom" TYPE="squashfs"
```



## openwrt启动过程

文档：

[Procd system init and daemon management](https://openwrt.org/docs/techref/procd)

[Preinit and Root Mount and Firstboot Scripts](https://openwrt.org/docs/techref/preinit_mount)

大致启动流程，Linux Kernel启动sbin/init：

- init启动/etc/inittab->/etc/init.d/rcS->/etc/rc.d/S*
- init启动procd

### Linux的0号进程启动/sbin/init

Linux Kernel的[init/main.c](https://github.com/torvalds/linux/blob/24aed09451270b6a2a78adf8a34918d12ffb7dcf/init/main.c#L1467)中执行`/sbin/init`，openwrt的init程序实现在`procd.git`仓库中的`initd`目录下：

```
-> initd/main.c, main()
-> initd/init.c, preinit()
    - fork()执行/etc/preinit脚本
    - fork()执行procd
```

### `/etc/preinit`shell脚本的行为

```
#!/bin/sh
# Copyright (C) 2006-2016 OpenWrt.org
# Copyright (C) 2010 Vertical Communications

# 解读：PREINIT环境变量不存在时执行/sbin/init进程
[ -z "$PREINIT" ] && exec /sbin/init

export PATH="/usr/sbin:/usr/bin:/sbin:/bin"
export DBGLVL=7

. /lib/functions.sh
. /lib/functions/preinit.sh
. /lib/functions/system.sh

boot_hook_init preinit_essential
boot_hook_init preinit_main
boot_hook_init failsafe
boot_hook_init initramfs
boot_hook_init preinit_mount_root

for pi_source_file in /lib/preinit/*; do
	. $pi_source_file
done

boot_run_hook preinit_essential

pi_mount_skip_next=false
pi_jffs2_mount_success=false
pi_failsafe_net_message=false

boot_run_hook preinit_main

```



### `procd`进程的行为

状态由`state.c`管理，与初始化有关的状态为：

- early：设备相关初始化

  1. watchdog_init()
  2. hotplug("/etc/hotplug.json") 
  3. procd_coldplug() 冷启动设备，在这函数里面切换到下一个状态

- ubus：启动ubusd

  1. watchdog_init(0)

  2. set_stdio("console")

  3. procd_connect_ubus() 里面在uloop里创建了个timer，定时连接ubus，连接上ubus后切换到下一个状态

  4. service_start_early("ubus", ubus_cmd, p?"ubus":NULL, p?"ubus":NULL) 将`/sbin/ubus`作为一个服务启动

- init：

  1. procd_inittab()
  2. procd_inittab_run("respawn")
  3. procd_inittab_run("askconsole")
  4. procd_inittab_run("askfirst")
  5. procd_inittab_run("sysinit")
  6. ulog_open(ULOG_SYSLOG, LOG_DAEMON, "procd");  输出log到syslog

Tips：

调试时为了方便，可以把log.h里的DEBUG宏换成：

```
#define DEBUG(level, fmt, ...)   ulog(LOG_NOTICE, fmt, ## __VA_ARGS__)
```

`coldplug.c`里会挂载

```
mount("devtmpfs", "/dev", "devtmpfs", MS_NOSUID, 0);
```

