tags:
- linux
- command
---



《The Linux Command Line 中文版》

https://www.kancloud.cn/thinkphp/linux-command-line/39431



---



mkdir 创建目录
cp 拷贝
cat 输出文件内容
stat 查看文件属性
wc 获取文件长度、字符数、行数
ll 罗列当前目录内容（-h 以K,M,G单位表示文件大小）
chmod 修改权限，常用开关-R递归，例子 chmod -R a+wr *
mv 移动文件
rm 删除,常用开关-f强制-r递归
ps 查看进程 常用开关-aux
kill 杀进程，用进程号

killall 杀进程，用程序名字

nohup 后台运行进程 nohup ./xx.sh >output 2>&1 &
find /home -name "abc.txt"
tail 查看指定文件末尾几行
which 获取指定文件的完整路径（$PATH中的）
shred 粉碎文件
tail 看文件尾部 -f参数看实时log日志（追加文件内容）
lsusb 查看usb设备
lsof 列出被打开的文件、被哪个应用打开

lspci  查看pci设备

file 查看文件类型（比如ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-uClibc.so.0, not stripped）
htop 查看哪个程序占用了cpu/ram资源
iotop 查看哪个程序阻塞了io资源

whereis 找二进制文件、其帮助文档的位置

hexdump 16进制查看（-C参数增加ASCII文本显示）

man 使用手册
info 比使用手册更详细的“电子书”

nano 文本编辑器

ssh 远程登入工具

diff 对比工具，`diff -r`对比文件夹

grep 筛选，-A显示筛选后若干行，-B显示筛选前若干行

## cat

cat拼接文件，连接文件，合并文件

```
$ cat file1.bin file2.bin
```



## mount



```
# 判断一个目录是否是挂载点
mountpoint -q /mnt
echo $?
```



## tar 解压压缩

.tar文件本身只是“归档”文件，把多个文件打包，而不带压缩；而.tar.gz文件是先把一些文件打包，然后用gzip压缩。

commands：

```
c  压缩
x  解压
t  列表
v  繁琐地打印一些信息
z  gzip
f  使用归档文件

创建/解压归档文件
$ tar -cf xxx.tar foo1 foo2
$ tar -xf xxx.tar

创建归档gzip压缩文件
$ tar -czf xxx.tar.gz foo1 foo2
$ tar -xzf xxx.tar.gz

查看文件列表：
$ tar -tvf xxx.tar
```

## linux校验值计算命令

```
# cd /usr/bin && find -name "*sum"
./cksum
./md5sum
./sha1sum
./sha256sum
./sha3sum
./sha512sum
```

cksum是CRC32


## 以别的用户身份执行命令

```
su - username -c "command" 
crontab -e -u username
```

## ps

查看实际使用内存

```
ps -o pid,comm,rss
```

## du

统计文件夹大小

例，深度1：

```
$ du --max-depth=1 -h /usr/
```



## watch

linux循环执行命令 2s执行一次

```
wait -n 2 “xxx”
```

## dmsg

设备相关log，常用于诊断设备故障，比如查看加载了哪些驱动、把什么硬件资源分配给了什么驱动。

例如usb设备的插拔信息、给pci设备加载了什么驱动。



## 通过网络更新系统时间

linux网络授时，使用NTP客户端完成；使用hwclock命令将时间写入主板：

```
$ sudo ntpdate -u ntp.api.bz
$ sudo hwclock -w
```



## install命令

在安装程序时比cp更方便的实用命令

```
相当于mkdir -p path/to/dst && cp src path/to/dst
$ install -D src path/to/dst
```



### 网络命令

```
arp = ip neighbor
ifconfig = ip address, ip link
netstat = ss
route = ip route
```

ifconfig等命令的package：
```
pacman -S net-tools dnsutils inetutils iproute2
```



## 待分类

archivemount 利用FUSE（用户层文件系统框架）将归档文件mount到文件系统中
gdb-multiarch   多架构gdb, 工具链中的gdb有问题的时候可以用