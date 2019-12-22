title: linux启动流程
date: 2019-06-19
categories:
- 计算机
- linux


---

## busybox构建的rootfs的linux启动流程

环境: 

kernel挂载rootfs后，运行linuxrc, busybox解析/etc/inittab配置:

```
# Startup the system
::sysinit:/bin/mount -t proc proc /proc
::sysinit:/bin/mount -o remount,rw /
::sysinit:/bin/mkdir -p /dev/pts /dev/shm
::sysinit:/bin/mount -a
::sysinit:/sbin/swapon -a
null::sysinit:/bin/ln -sf /proc/self/fd /dev/fd
null::sysinit:/bin/ln -sf /proc/self/fd/0 /dev/stdin
null::sysinit:/bin/ln -sf /proc/self/fd/1 /dev/stdout
null::sysinit:/bin/ln -sf /proc/self/fd/2 /dev/stderr
::sysinit:/bin/hostname -F /etc/hostname
# now run any rc scripts
::sysinit:/etc/init.d/rcS

# Put a getty on the serial port
console::respawn:/sbin/getty -L  console 0 vt100 # GENERIC_SERIAL

# Stuff to do for the 3-finger salute
#::ctrlaltdel:/sbin/reboot

# Stuff to do before rebooting
::shutdown:/etc/init.d/rcK
::shutdown:/sbin/swapoff -a
::shutdown:/bin/umount -a -r

```

总结启动流程:

1. 内核挂载rootfs, 执行linuxrc, 由它的配置文件/etc/inittab确定剩下的启动流程
2. 先mount构造目录树:  mount -a会挂载/etc/fstab中所有节点
3. 执行/etc/init.d/rcS, rcS会按顺序遍历/etc/init.d/S*
4. 使用getty, 将tty挂在串口上

用户登入后, 才会执行/etc/profile