---



一些流行的 Linux 发行版包管理器命令的对应关系
https://wiki.archlinux.org/index.php/Pacman/Rosetta_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)



## pacman系

pacman是arch系下的包管理工具

Archlinux 的灵魂──PKGBUILD、AUR 和 ABS
https://blog.csdn.net/taiyang1987912/article/details/41457333#

```
# 更新所有包
pacman -Syu

# 搜索包
pacman -Ss xxx

# 安装包
pacman -S xxx
# 安装二进制包
pacman -U xxx.tar.zst

# 删除软件包，顺便移除没被其他包依赖的依赖包
pacman -Rs xxx
```

### pacman自动更换中国源

```bash
# pacman-mirrors -c China
# pacman -Syy
```

### AUR是非官方提供的包

为了安全，一般不是直接发布二进制包，而是一些包含编译脚本的信息。

使用`yay`可以方便地使用AUR：

```
pacman -S yay
```

yay支持pacman风格的命令，挪过来就能用。

### 将debian的deb包转成arch package格式

> refer: https://ostechnix.com/convert-deb-packages-arch-linux-packages/

```
$ yay -S debtap
$ sudo debtap -u
$ debtap intelmas_1.7.130-0_amd64.deb
$ sudo pacman -U sudo pacman -U intelmas-1.7.130-1-x86_64.pkg.tar.zst
```



## apt


```bash
# 列出包中安装的文件位置
dpkg -L packagename
# 检查是否安装成功
dpkg -l | grep packagename
# 同上
apt list --installed | grep packagename
```



### auto-apt

源码编译安装时，自动生成deb包方便管理

使用auto-apt 和 checkinstall，具体命令如下
```bash
#安装auto-apt和checkinstallapt install auto-apt checkinstall
#在源码目录中auto-apt run ./configure
make
checkinstall
```

这样会生成一个deb包，卸载和重新安装就非常方便了

```bash
#完全卸载 (packagename具体的名字在checkintall完成之后会有提示）
dpkg -r packagename

#用生成的deb包重新安装
dpkg -i ***.deb
```



### apt解决坏依赖

比如提示
```
The following packages have unmet dependencies:
libpcre3-dev : Depends: libpcre3 (= 1:8.31-2ubuntu2) but 1:8.31-2ubuntu2.1 is to be installed
```

可以强制指定版本
```
sudo apt-get install libpcre3=1:8.31-2ubuntu2 libpcre3-dev=1:8.31-2ubuntu2
```