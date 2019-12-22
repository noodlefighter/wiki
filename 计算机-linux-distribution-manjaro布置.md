title: manjaro布置
date: 2019-09-24
categories:
- 计算机
- linux
- distribution




---

> TODO 搬移



### 网络命令

```
arp = ip neighbor
ifconfig = ip address, ip link
netstat = ss
route = ip route
```

### ibus配置

配置文件在`~/.config/ibus`

.xprofile：
```
export GTK_IM_MODULE=ibus
export XMODIFIERS=@im=ibus
export QT_IM_MODULE=ibus
ibus-daemon -d -x
```

默认输入法为第一个，顺序在dconf中配置：`desktop/ibus/general/engines-order`。

### 安装字体



```
mkdir /usr/share/fonts/<font_name>
cd /usr/share/fonts/<font_name>
mkfontscale
mkfontdir
fc-cache -fv
```

