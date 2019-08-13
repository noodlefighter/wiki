

---

xxd是个十六进制编辑器，可以完成二进制文件与十六进制文本的转换



## 文件转十六进制文本



```
$ xxd mount_mysdk.sh 
00000000: 2321 2f62 696e 2f62 6173 680a 0a73 7368  #!/bin/bash..ssh
00000010: 6673 206d 7063 406d 7973 646b 3a2f 686f  fs mpc@mysdk:/ho
00000020: 6d65 2f6d 7063 2f77 6f72 6b73 7061 6365  me/mpc/workspace
00000030: 7320 7e2f 6d79 7364 6b0a 0a              s ~/mysdk..
```

常用选项:

```
-p  不加空格地输出一整块hex
-l  输出几个字节后结束，如-l12
-i  以c语言格式输出
-g  几个字节为一组
-c  每行输出多少字节
-b  以二进制格式输出
```

## 文件转C语言格式数组

```
$ xxd -g 1 -i -u -l 10000000 nm.ts
```

## 将文本导回二进制文件

```
# 将不带空格的hex文本导回二进制，也就是-p参数生成的文本，如：
$ xxd -r -p xxx.txt
```

例如对于这样的十六进制文本：

```
    0x31, 0x5d, 0xfa, 0x52, 0xa4, 0x93, 0x52, 0xf8, 0xf5, 0xed, 0x39, 0xf4, 0xf8, 0x23, 0x4b, 0x30,
    0x11, 0xa2, 0x2c, 0x5b, 0xa9, 0x8c, 0xcf, 0xdf, 0x19, 0x66, 0xf5, 0xf5, 0x1a, 0x6d, 0xf6, 0x25,
    0x89, 0xaf, 0x06, 0x13, 0xdc, 0xa4, 0xd4, 0x0b, 0x3c, 0x1c, 0x4f, 0xb9, 0xd3, 0xd0, 0x63, 0x29,
```

最简单的方法是

```
$ cat hextest |sed 's/ //g' |sed 's/,//g' |sed 's/0x//g' |xxd -r -p > bintest
```

## xxd配合vim使用

打开一个二进制文件:

```
% vim -b xxx.bin
```

转换成十六进制文本：

```
:%!xxd
```

转回来：
```
:%!xxd -r
```

