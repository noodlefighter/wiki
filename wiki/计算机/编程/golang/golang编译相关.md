

## golang交叉编译

linux+arm+静态链接+缩减大小：

```
$ env GOOS=linux GOARCH=arm go build -ldflags="-extldflags=-static -s" -o rtsp-simple-server_arm
```

-s     去掉 输出文件 中的 全部 符号信息

## golang二进制尺寸优化

>  refers:
>
> - https://github.com/xaionaro/documentation/blob/master/golang/reduce-binary-size.md

```
$ go build -a -gcflags=all="-B" -ldflags="-w -s"
$ upx helloworld
```

