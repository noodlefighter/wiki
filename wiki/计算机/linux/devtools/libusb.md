

## libusb开启调试

编译的时候开启选项`--enable-system-log`和`--enable-debug-log`：

```
    ./configure --host=${GNU_TARGET_NAME} \
                --prefix=${DESTROOT} \
                --disable-doc \
                --disable-docs \
                --disable-udev \
                --enable-system-log \
                --enable-debug-log \
                --enable-examples-build \
                --disable-documentation
```

日志会输出到`syslog`中，如果在使用的rootfs由busybox提供，则需要启动`syslogd`服务。

查看`/var/log/message`：

```
# cat /var/log/messages
Jan  1 00:24:43 (none) syslog.info syslogd started: BusyBox v1.22.1
Jan  1 00:24:50 (none) user.debug testlibusb1: [timestamp] [threadID] facility level [function call] <message>
Jan  1 00:24:50 (none) user.debug testlibusb1: --------------------------------------------------------------------------------
Jan  1 00:24:50 (none) user.debug testlibusb1: [ 0.000141] [00000083] libusb: debug [libusb_init] created default context
Jan  1 00:24:50 (none) user.debug testlibusb1: [ 0.000697] [00000083] libusb: debug [libusb_init] libusb v1.0.22.11312
Jan  1 00:24:50 (none) user.err testlibusb1: [ 0.001117] [00000083] libusb: error [op_init] could not find usbfs
```

