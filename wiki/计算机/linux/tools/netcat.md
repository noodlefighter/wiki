

---

## netcat的版本

* bsd-netcat
* gnu-netcat
* [nmap-netcat](https://nmap.org/ncat/)(ncat)

## nmap的netcat(ncat)

nmap的netcat可以这样实现一个echo-server：

```
$ ncat -l 2000 --keep-open --exec "/bin/cat"
```

作为服务器，监听一个端口，连接的客户端间发送的消息会互通（像一个router）：

```
$ ncat --broker --listen -p 12345
```

服务器监听1234、1235端口，连接1234的客户端发送的数据，转发至连接到1235的客户端：

```
$ ncat --keep-open --listen -p 1234 | ncat --keep-open --listen -p 1235
```



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
