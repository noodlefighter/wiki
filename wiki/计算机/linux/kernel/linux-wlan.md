# Linux中WLAN（WIFI）相关



## Linux WLAN 用户态配置

Linux用户态配置WLAN可以参考ArchLinux的WIKI：

https://wiki.archlinux.org/index.php/Network_configuration/Wireless

现在主要用iw工具配置WLAN，iw使用方法参考：

https://wireless.wiki.kernel.org/en/users/documentation/iw



iw 无线通用配置工具

hostapd 开启AP的工具，AP端用

wpa_supplicant WPA实用连接工具，STA端用



## Wireless-Extensions(LWE)

Linux中老的无线API，无线驱动需要实现这些API，对应的用户态程序是iwconfig。

这个子系统已经不会添加新功能，只会修bug。

> 印象中老到2.6.x的内核就用的这些API



## cfg80211和nl80211

cfg80211/nl80211是Wireless-Extensions的替代。

cfg80211是内核态中的一套API接口，用于配置无线设备，驱动实现cfg80211时只需填入一些回调，而之前的LWE接口为了能给用户态用，需要自己实现ioctl。

nl80211是给用户态的API，它通过调用cfg80211接口为用户态提供功能。

WLAN驱动需要实现cfg80211接口，才能通过iw工具配置无线网络，比如博通自己家有broadcom-wl所以对iw命令支持就不是很好，比如可能就无法通过iw工具设置国家码。

现在iw、crda、hostapd、wpa_supplicant等都支持，他们通过libnl库访问nl80211接口。

> refers:
> https://wireless.wiki.kernel.org/en/developers/documentation/cfg80211
> https://wireless.wiki.kernel.org/en/developers/documentation/nl80211



## 关于WLAN的国家码（country_code/region）


> https://wireless.wiki.kernel.org/en/developers/Regulatory

每个国家的无线管制不一样，为了让用户能调整配置至符合当地法规，需要能在用户态修改国家码。

### 如何配置国家码？

以前是通过载入内核模块驱动时传入`ieee80211_regdom=US`这样的参数配置国家码的，而现在已经不推荐这样做了，用`iw reg set CN`这样的命令就能配置国家码

有的厂商没完全实现cfg80211接口所以没法用iw配置国家码，这时可以修改`nvram.txt`实现，比如博通驱动`ccode=CN`。

### 什么是CRDA（Central Regulatory Domain Agent）？

机制的目的：CRDA用于动态更新regdb（各国家的管制信息数据库），允许将regdb放在用户态文件系统中，以前这些信息是内置在Linux内核中的，有CRDA后无需重新编译内核也能更新regdb。

Linux内核的Kconfig中有个`CONFIG_CFG80211_INTERNAL_REGDB`，配置后就可以不用CRDA了（不过我没找到配置的方法，怎么设都始终为n）

https://wireless.wiki.kernel.org/en/developers/regulatory/crda