

---



> TODO 处理掉这些链接

https://blog.csdn.net/liyuanbhu/article/details/72851068
交叉编译
https://blog.csdn.net/xukai871105/article/details/37345857
https://blog.csdn.net/mantis_1984/article/details/52847435
https://blog.csdn.net/kl222/article/details/49705143?utm_source=blogxgwz6

引用库libusb-1.0时，Makefile中取参数例子：
```
# use pkg-config
CFLAGS  += $(shell pkg-config libusb-1.0 --cflags)
LDFLAGS += $(shell pkg-config libusb-1.0 --libs)
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