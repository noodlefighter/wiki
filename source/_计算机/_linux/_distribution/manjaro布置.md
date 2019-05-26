

---

> TODO 搬移

Archlinux 的灵魂──PKGBUILD、AUR 和 ABS
https://blog.csdn.net/taiyang1987912/article/details/41457333#

一些流行的 Linux 发行版包管理器命令的对应关系
https://wiki.archlinux.org/index.php/Pacman/Rosetta_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

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

aur上有个ttf-consolas-with-yahei

```
mkdir /usr/share/fonts/<font_name>
cd /usr/share/fonts/<font_name>
mkfontscale
mkfontdir
fc-cache -fv
```

### 调优资源调度

https://www.linuxidc.com/Linux/2017-02/141138.htm

> TODO: 搬移