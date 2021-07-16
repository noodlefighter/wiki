## 查看分区UUID等信息

```
$ blkid
/dev/nvme0n1p1: UUID="1f118546-b8f0-4d80-b4da-ded14522c7f8" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="07b9804d-01"
/dev/sda1: UUID="FA68-E285" BLOCK_SIZE="512" TYPE="vfat" PARTUUID="a26afd37-c6ca-4e5c-bbd4-9ca66929e785"
```

## mount

判断一个目录是否是挂载点：

```
mountpoint -q /mnt
echo $?
```

## mount 回环设备（lookback device）

需要把镜象文件到本地文件树，则需要建立回环设备。

### 手动建立回环设备

```
# losetup -f --show raspios.img
/dev/loop3
# fdisk -l /dev/loop3
Disk /dev/loop3: 3.8 GiB, 4009754624 bytes, 7831552 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xe8af6eb2

Device       Boot  Start     End Sectors  Size Id Type
/dev/loop3p1        8192  532479  524288  256M  c W95 FAT32 (LBA)
/dev/loop3p2      532480 7831551 7299072  3.5G 83 Linux

卸载回环设备
# losetup -d /dev/loop3
```



### mount命令直接挂载分区的镜象

如果直接是某个分区的镜象，可以直接用`mount -o loop`，会自动建立回环设备：

```
# mount /tmp/disk.img /mnt -o loop,rw
```

或者已知分区的offset：

```
# mount xxx.img -o loop,offset=$(($P0_START*$SECTOR_SIZE)),rw $2
```

### mount命令挂载多分区的镜象

先用fdisk拿到文件系统分区的位置（也可以先`losetup`再`fdisk -l /dev/loopXXX`，不过麻烦，还得记得卸载掉这个设备）：

```
# fdisk -l raspios.img
Disk raspios.img: 3.8 GiB, 4009754624 bytes, 7831552 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xe8af6eb2

Device                                           Boot  Start     End Sectors  Size Id Type
images/2021-01-11-raspios-buster-armhf-lite.img1        8192  532479  524288  256M  c W95 FAT32 (LBA)
images/2021-01-11-raspios-buster-armhf-lite.img2      532480 7831551 7299072  3.5G 83 Linux
```

信息显示，一个Sectors的大小是512Bytes，则分区0的起始地址是`$(($P0_START*$SECTOR_SIZE))`即`8192*512`，多分区时记得带上`sizelimit`以避免`overlapping loop device exists`错误，见[这个讨论串](https://www.raspberrypi.org/forums/viewtopic.php?t=190154):

```
# mount raspios.img  -o loop,offset=$((532480*512)),sizelimit=$((7299072*512)),rw /media/rpi/
# mount raspios.img  -o loop,offset=$((8192*512)),sizelimit=$((524288*512)),rw  /media/rpi/boot
```



## 缩小镜象文件

```
# 创建回环设备，但不挂载
losetup /dev磁盘管理/loop0 ./qt.img
# 置零空闲数据
zerofree -v /dev/loop0
# 断开回环设备
losetup -d /dev/loop0
# 文件系统检查
e2fsck -f qt.img
# 缩减空间
resize2fs -M qt.img
```



## Linux下用mdadm创建soft raid 软件磁盘阵列

> refer: https://www.digitalocean.com/community/tutorials/how-to-create-raid-arrays-with-mdadm-on-ubuntu-16-04

Find the active arrays in the `/proc/mdstat` file by typing:

```
$ cat /proc/mdstat
```

移除阵列：

```
停止阵列，删除阵列
$ sudo mdadm --stop /dev/md0
$ sudo mdadm --remove /dev/md0

清除超级块
$ sudo mdadm --zero-superblock /dev/sdc
$ sudo mdadm --zero-superblock /dev/sdd
```

创建raid0阵列：

```
$ sudo mdadm --create --verbose /dev/md0 --level=0 --raid-devices=2 /dev/sda /dev/sdb
```

