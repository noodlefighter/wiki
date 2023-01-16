## 用qemu和chroot调试异构rootfs

> 参考：使用QEMU chroot进行固件本地调试 https://cloud.tencent.com/developer/article/1552161



qemu-user-static使用Linux的**binfmt_misc**机制，允许识别任意可执行文件格式，并将其传递给特定的用户空间应用程序。

> QEMU User Mode 二进制翻译系统原理分析及使用方法: https://zhuanlan.zhihu.com/p/392753064
>
> 如果要使用这个功能的话，首先要绑定binfmt_misc，可以通过以下命令来绑定：
>
> ```text
> mount binfmt_misc -t binfmt_misc /proc/sys/fs/binfmt_misc
> ```
>
> 这样绑定的话，系统重新启动之后就失效了。如果想让系统每次启动的时候都自动绑定的话，可以往 /etc/fstab 文件中加入下面这行：
>
> ```text
> none  /proc/sys/fs/binfmt_misc binfmt_misc defaults 0 0
> ```



比如使用qemu-debootstrap创建的debian根文件系统，qemu-debootstrap会多做一件事，把qemu-user-static拷进去，所以可以直接chroot进去：

```
sudo apt-get update
sudo apt-get install debootstrap qemu qemu-user-static
sudo qemu-debootstrap --arch armhf bionic armhf-chroot
sudo chroot armhf-chroot

uname -m 
```



而我们自己构建的rootfs，就需要自己拷贝了，比如我现在目标系统是32位的arm：

```
$ cd tmp/work/ebsx_imx6ull-poky-linux-gnueabi/GDEBS-ADA-01-image/1.0-r0/rootfs
$ cp /usr/bin/qemu-arm-static ./usr/bin/
$ sudo chroot .
```

