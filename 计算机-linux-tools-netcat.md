title: netcat
date: 2019-12-06
categories:
- 计算机
- linux
- tools




---

## netcat的两个版本

一般发行版仓库里有两个版本:
* bsd-netcat
* gnu-netcat

gnu这个用的时候得注意这样是不行的, 得用-p参数指定端口
```
nc -l 9898
```
很好, 我选择bsd的实现.



## 类似的工具

nc缺少一些功能如端口转发，类似工具：

https://nmap.org/ncat/

http://www.dest-unreach.org/socat/doc/socat.html



## 用nc测试不断地连接、断开

```
watch -n 0.1 "echo sdfadf |nc -w0 -N localhost 4646"
```



## socat - Multipurpose relay

http://www.dest-unreach.org/socat/
http://www.dest-unreach.org/socat/doc/socat.html

“多用途中继”,看着是想代替netcat.

### 使用socat监听unix socket

```
$ sudo mv /path/to/sock /path/to/sock.original
$ sudo socat -t100 -x -v UNIX-LISTEN:/path/to/sock,mode=777,reuseaddr,fork UNIX-CONNECT:/path/to/sock.original
```

例：
```
$ sudo socat -t100 -x -v UNIX-LISTEN:/var/run/ubus.sock,mode=777,reuseaddr,fork UNIX-CONNECT:/var/run/ubus.sock.original

< 2019/11/28 19:37:35.355383  length=12 from=0 to=11
 00 00 00 00 8a fe d1 a8 00 00 00 04              ............
--
> 2019/11/28 19:37:35.355631  length=12 from=0 to=11
 00 04 00 01 00 00 00 00 00 00 00 04              ............
--
< 2019/11/28 19:37:35.355823  length=20 from=12 to=31
 00 01 00 01 00 00 00 00 00 00 00 0c 01 00 00 08  ................
 00 00 00 00                                      ....
--
```
