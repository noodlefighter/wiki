

linux内核并不管理DNS缓存，具体服务有多种选择

## Linux刷新DNS缓存

参考：https://www.maketecheasier.com/flush-dns-cache-linux/

先systemctl看看存在什么服务，比如：nscd（glibc提供），dnsmasq，named，systemd-resolve（systemd提供）

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


