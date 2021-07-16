

---

> TODO

https://wiki.archlinux.org/index.php/Udev_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

http://webpages.charter.net/decibelshelp/LinuxHelp_UDEVPrimer.html

https://blog.csdn.net/chituhuan/article/details/52383610



在用户态管理设备接入、移除的程序



## udev规则编写(udev rule)

参考：[使用 udev 高效、动态地管理 Linux 设备文件](https://www.ibm.com/developerworks/cn/linux/l-cn-udev/index.html) / 规则文件编写可参考`man udev`



配置文件位置：`/usr/lib/udev/rules.d`系统自带的规则，会随系统更新而更新；`/etc/udev/rules.d`用户自定义规则。规则文件命名如`50-udev-default.rules`，自定义中如果有同名文件，会覆盖自带的规则。

大概的逻辑就是：匹配-->执行操作，比如：

**为指定大小的磁盘产生符号链接的规则**

```
SUBSYSTEM=="block", SYSFS{size}=="71096640", SYMLINK ="my_disk"
```

**通过外部命令为指定序列号的磁盘产生设备文件的规则**

```
KERNEL=="sd*[0-9]", PROGRAM=="/lib/udev/scsi_id -g -s %p", \
RESULT=="35000c50000a7ef67", NAME +="root_disk%n"
```

相关命令：

```
# 查看某设备文件的信息（可以用来获取sysfs路径） ，以便编写规则
udevadm info /dev/ttyUSB0
# 测试规则
udevadm test --action="add" /devices/pci0000:00/0000:00:1a.0/usb1/1-1/1-1.3/1-1.3.1/1-1.3.1:1.0/ttyUSB0/tty/ttyUSB0
# 重新载入规则
udevadm control --reload-rules && udevadm trigger
```

例子，`99-tty-permission.rules`，设置所有ttyUSB设备权限为0777：

```
KERNEL=="ttyUSB*[0-9]", MODE="0777"
```

例子，mount USB存储设备（via: https://unix.stackexchange.com/questions/44454/how-to-mount-removable-media-in-media-label-automatically-when-inserted-with）：

```
# Add symlink /dev/usbdisks/<label> to /dev/sd[a-z][1-9] 
# if partition has a label
# Add symlink /media/usb/<label> to /media/autousb/<label>
# for automounter support
ACTION=="add", KERNEL=="sd*", ENV{DEVTYPE}=="partition", \
    ENV{ID_BUS}=="usb", ENV{ID_FS_LABEL_ENC}=="?*", \
    SYMLINK+="usbdisks/$env{ID_FS_LABEL_ENC}", MODE:="0660", \
    RUN+="/bin/rm /media/usb/$env{ID_FS_LABEL_ENC}", \
    RUN+="/bin/ln -sf /media/autousb/$env{ID_FS_LABEL_ENC} /media/usb/$env{ID_FS_LABEL_ENC}"

# Fallback: If partition has a NO label, use kernel name (sd[a-z][1-9])
ACTION=="add", KERNEL=="sd*", ENV{DEVTYPE}=="partition", \
    ENV{ID_BUS}=="usb", ENV{ID_FS_LABEL_ENC}!="?*", \
    SYMLINK+="usbdisks/%k", MODE:="0660", \
    RUN+="/bin/rm /media/usb/%k", \
    RUN+="/bin/ln -sf /media/autousb/%k /media/usb/%k"

# Some FileSystems emit a "change" event when they are unmounted.
# UDEV seems to delete the device symlink in this case :-(
# So we need to re-create it here
ACTION=="change", KERNEL=="sd*", ENV{DEVTYPE}=="partition", \
    ENV{ID_BUS}=="usb", ENV{ID_FS_LABEL_ENC}=="?*", \
    SYMLINK+="usbdisks/$env{ID_FS_LABEL_ENC}", MODE:="0660"

# Fallback: If partition has NO label, use kernel name
ACTION=="change", KERNEL=="sd*", ENV{DEVTYPE}=="partition", \
    ENV{ID_BUS}=="usb", ENV{ID_FS_LABEL_ENC}!="?*", \
    SYMLINK+="usbdisks/%k", MODE:="0660"


# When device is removed, also remove /media/usb/<label>
ACTION=="remove", KERNEL=="sd*", ENV{DEVTYPE}=="partition", \
    ENV{ID_BUS}=="usb", ENV{ID_FS_LABEL_ENC}=="?*", \
    RUN+="/bin/rm /media/usb/$env{ID_FS_LABEL_ENC}"

# Fallback: If partition has no label, remove /media/usb/%k
ACTION=="remove", KERNEL=="sd*", ENV{DEVTYPE}=="partition", \
    ENV{ID_BUS}=="usb", ENV{ID_FS_LABEL_ENC}!="?*", \
    RUN+="/bin/rm /media/usb/%k"
```

例，自动 mount 特定分区：

```
ACTION=="add", ENV{DEVTYPE}=="partition", \
    ENV{ID_PART_ENTRY_UUID}=="65e1a058-7993-48f1-89ab-e7f5384bd335" \
    RUN+="/bin/mount /dev/disk/by-partuuid/$env{ID_PART_ENTRY_UUID} /mnt/chiaplots" \
    RUN+="/bin/chmod 777 /mnt/chiaplots"

ACTION=="remove", ENV{DEVTYPE}=="partition", \
    ENV{ID_PART_ENTRY_UUID}=="65e1a058-7993-48f1-89ab-e7f5384bd335" \
    RUN+="/bin/umount /mnt/chiaplots" 
```

