# Linux内核编译



Linux内核的Makefiles说明文档:

https://www.kernel.org/doc/Documentation/kbuild/makefiles.txt



## 交叉编译Linux内核

```
$ make ARCH=arm CROSS_COMPILE=arm-linux-eabi-
```

