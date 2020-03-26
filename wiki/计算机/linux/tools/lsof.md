

# lsof命令 用于查看处于打开状态的文件

`lsof`命令可以列出所有正在打开的文件，可以用它的选项对这些文件进行筛选。

>  ref: https://www.tecmint.com/10-lsof-command-examples-in-linux/

## 列出指定进程PID打开的文件

```
# lsof -p 1
COMMAND PID USER   FD      TYPE             DEVICE SIZE/OFF       NODE NAME
systemd   1 root  cwd       DIR              259,1     4096          2 /
systemd   1 root  rtd       DIR              259,1     4096          2 /
systemd   1 root  txt       REG              259,1  1537896    4074804 /usr/lib/systemd/systemd
systemd   1 root  mem       REG              259,1  1329272    4077522 /usr/lib/libm-2.31.so
systemd   1 root  mem       REG              259,1   169936    4082603 /usr/lib/libudev.so.1.6.15
systemd   1 root  mem       REG              259,1  1574704    4074067 /usr/lib/libunistring.so.2.1.0
systemd   1 root  mem       REG              259,1    67504    4073829 /usr/lib/libjson-c.so.4.0.0

```

## 列出特定用户打开的文件

```
仅r用户
# lsof -u r

排除root用户
# lsof -u^root
```

## 列出使用TCP端口的进程

用`-i`参数筛选网络相关的文件：

```
[46][protocol][@hostname|hostaddr][:service|port]
```

```
# lsof -i TCP:22
# lsof -i TCP:1-1024
```

## 杀死某用户的所有进程

```
# kill -9 `lsof -t -u r`
```

