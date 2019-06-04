

---



> TODO 处理掉这些链接


交叉编译
https://blog.csdn.net/mantis_1984/article/details/52847435
https://blog.csdn.net/kl222/article/details/49705143?utm_source=blogxgwz6

## 用处

> via: <https://zh.wikipedia.org/wiki/Pkg-config>

pkg-config 是一个在源代码编译时查询已安装的库的使用接口的计算机工具软件。pkg-config原本是设计用于Linux的，但现在在各个版本的BSD、windows、Mac OS X和Solaris上都有着可用的版本。

它输出已安装的库的相关信息，包括：

* C/C++编译器需要的输入参数
* 链接器需要的输入参数
* 已安装软件包的版本信息

## .pc文件

每个.pc文件描述一个软件包，例如：

```
prefix=/home/r/lede_lean/staging_dir/host
exec_prefix=/home/r/lede_lean/staging_dir/host
libdir=${exec_prefix}/lib
includedir=${prefix}/include

Name: json-c
Description: JSON implementation in C
Version: 0.12.1
Requires: 
Libs:  -L${libdir} -ljson-c
Cflags: -I${includedir}/json-c
```

以live555为例，pkg-config方式安装动态库的例子：

Makefile

```
install_shared_libraries:
install -d $(DESTDIR)$(LIBDIR)/pkgconfig
sed "s#@PREFIX@#$(PREFIX)#;s#@LIBDIR@#$(LIBDIR)#;s#@VERSION@#$(VERSION)#" live555.pc.in > $(DESTDIR)$(LIBDIR)/pkgconfig/live555.pc
chmod 644 $(DESTDIR)$(LIBDIR)/pkgconfig/live555.pc
```

live555.pc.in

```
prefix=@PREFIX@
libdir=@LIBDIR@
includedir=${prefix}/include

Name: live555
Description: multimedia RTSP streaming library
Version: @VERSION@
Cflags: -I${includedir}/liveMedia -I${includedir}/groupsock -I${includedir}/BasicUsageEnvironment -I${includedir}/UsageEnvironment
Libs: -L${libdir} -lliveMedia -lgroupsock -lBasicUsageEnvironment -lUsageEnvironment
```

## 使用方法

最常用：

```
$ pkg-config --cflags json-c
-I/usr/include/json-c
$ pkg-config --libs json-c
-ljson-c
```

Makefile中取参数例子，引用库libusb-1.0：

```
# use pkg-config
CFLAGS  += $(shell pkg-config libusb-1.0 --cflags)
LDFLAGS += $(shell pkg-config libusb-1.0 --libs)
```

## 遇到的问题

### 明明存在.pc文件，但pkg-config搜索不到

PC上大多数软件的.pc都会装在`/usr/lib/x86_64-linux-gnu/pkgconfig/`里，但Mint Linux就没在PKG_CONFIG_PATH里默认放好路径，应该是个bug，手动加在`/etc/profile`里即可，比如：

```
export PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig/:PKG_CONFIG_PATH
```

