title: lrzsz
date: 2019-06-12
categories:
- 计算机
- linux
- tools




---



lrzsz支持Zmodem协议收/发文件, 做服务端.

```
# Zmodem接收文件
rz
# Zmodem发送文件
sz
```

Zmodem协议: 串流式（streaming）传输方式，传输速度较快，而且还具有自动改变区段大小和断点续传、快速错误侦测

另外还有支持Xmodem的rx/sx命令

## linux客户端

minicom支持各种协议收发文件: 

Ctrl+A S: 发送文件

Ctrl+A R: 接收文件

## Windows客户端

Xshell和mobaxterm都有这方面支持