

mDNS是Apple公司的局域网设备发现协议。



## Avahi

众多发行版的选择：

```
服务
$ avahi-daemon

扫描
avahi-browse -a
avahi-discover

```

依赖[nss-mdns](https://github.com/lathiat/nss-mdns)库，库本身很轻量。



## mDNSResponder

https://opensource.apple.com/tarballs/mDNSResponder/

源码中有个mDNSPosix目录可以在Linux下编译运行，感觉维护得并不是很好，新发的版本（1096）我这无法编译成功，旧版本（878）在我的电脑上编译出来后执行发生段错误。



