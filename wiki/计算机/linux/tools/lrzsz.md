

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



## 双方均为Linux时收发实例

我做了一个脚本

```
# tx/rx with ZMODEM
# example 1) sendz /dev/ttyUSB0 a.txt b.txt c.txt
# example 2) sendz /dev/ttyUSB0 *.ko
# example 3) zrecv /dev/ttyUSB0
__zmodem_szrz() {
        DEV=$2
        if [ $1 == 'zsend' ]; then
                CMD=sz
        elif [ $1 == 'zrecv' ]; then
                CMD=rz
        else
                echo "Wrong command."
                return 1
        fi
        stty -F $DEV 115200
        shift 2
        $CMD $* > $DEV < $DEV
}
zsend() {
        __zmodem_szrz zsend $*
}
zrecv() {
        __zmodem_szrz zrecv $*
}
```



## Windows

Xshell和mobaxterm都有这方面支持