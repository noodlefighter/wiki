

linux内核并不管理DNS缓存，具体服务有多种选择

## Linux刷新DNS缓存

参考：https://www.maketecheasier.com/flush-dns-cache-linux/

先systemctl看看存在什么服务，比如：nss-lookup，nscd（glibc提供），dnsmasq，named，systemd-resolve（systemd提供）

存在服务的话：

```
# systemctl restart <那个服务，比如dnsmasq>
```

不存在服务时：

```
# nscd -K
# nscd

# systemd-resolve --flush-caches
```



## ubuntu的dns缓存

> refer: https://www.freedesktop.org/software/systemd/man/systemd-resolved.service.html

查看`/etc/resolv.conf`，会看到：

```
nameserver 127.0.0.53
```

对应着本地的一个**systemd-resolved**服务（详见refer），出了问题应该去看它的日志，以及用`resolvctl`进行操作。

