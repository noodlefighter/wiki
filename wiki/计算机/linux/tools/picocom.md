

## picocom是个很轻的tty/pty工具

基本使用：

```
$ picocom /dev/ttyUSB0 -b 115200
```

`ctrl+a`进入选单，`ctrl+a,h`看帮助，`ctrl+a,q`退出...



## picocom使用十六进制模式

设置HEX显示模式：

```
$ picocom --imap spchex,nrmhex,8bithex
```

使用`ctrl+a,w`写入十六进制数据



## 使用 picocom dump 串口原始数据（raw 数据）

```
$ picocom /dev/ttyUSB0 -b 115200 --quiet > dump.bin
```

`--quiet`参数避免打出初始化信息

