---



## debian系下的包管理器



```bash
# 列出包中安装的文件位置
dpkg -L packagename
# 检查是否安装成功
dpkg -l | grep packagename
# 同上
apt list --installed | grep packagename
```



## auto-apt

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



## apt解决坏依赖

比如提示
```
The following packages have unmet dependencies:
libpcre3-dev : Depends: libpcre3 (= 1:8.31-2ubuntu2) but 1:8.31-2ubuntu2.1 is to be installed
```

可以强制指定版本
```
sudo apt-get install libpcre3=1:8.31-2ubuntu2 libpcre3-dev=1:8.31-2ubuntu2
```