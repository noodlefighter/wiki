
---

清华镜象服务
https://tuna.moe/

启动过程
https://www.cnblogs.com/image-eye/archive/2011/08/19/2145858.html
https://blog.csdn.net/kebu12345678/article/details/77091927

DTS资料：
https://www.raspberrypi.org/documentation/configuration/device-tree.md#part4.6

busybox
https://www.ibm.com/developerworks/cn/linux/l-busybox/

gdbServer + gdb 调试
https://www.cnblogs.com/Dennis-mi/articles/5018745.html

DBus
https://www.cnblogs.com/wuyida/p/6299998.html
https://www.freedesktop.org/wiki/Software/dbus/

和菜鸟一起学linux子系统
https://blog.csdn.net/eastmoon502136/column/info/linux-child-system

--- 

和菜鸟一起学linux系列文章
https://blog.csdn.net/eastmoon502136/article/list/6?t=1&orderby=UpdateTime

内核源码之基础准备篇
https://blog.csdn.net/eastmoon502136/article/details/8711104

---


Linux学习教程 - 运维视角，章节划分合理，适合参考
http://c.biancheng.net/linux_tutorial/

虚拟内存
https://sylvanassun.github.io/2017/10/29/2017-10-29-virtual_memory/

linux device class
https://mirrors.edge.kernel.org/pub/linux/kernel/people/mochel/doc/text/class.txt

linux下的动态链接文件
https://www.cnblogs.com/lidabo/p/4376708.html

Linux 线程模型的比较：LinuxThreads 和 NPTL
https://www.ibm.com/developerworks/cn/linux/l-threading.html

linux内核模块编写教程
http://www.tldp.org/LDP/lkmpg/2.6/html/

---

交叉编译相关


无线管理工具-iw
https://blog.csdn.net/qq_21792169/article/details/51224777

交叉编译库依赖问题的解决方法
https://blog.csdn.net/openblog/article/details/7449991

自己构建交叉编译工具链（GCC、AR之类，主要是可以自定义c库）
http://www.embeddedlinux.org.cn/emb-linux/system-development/201708/12-7114.html

交叉编译时的sysroot问题
http://www.eetop.cn/blog/html/52/51552-33478.html

crosstool-ng/buildroot/embtoolkit
https://www.embtoolkit.org/community.html

---

LFS项目，有适合需要交叉编译的子项目
http://www.linuxfromscratch.org/

---

关于目标板和开发机（服务器）之间根目录系统的同步，应该有以下方案：

* uboot从远程NFS启动
* 启动本地系统后连接网络，进行增量同步
* 启动本地系统后连接网络，下载根目录镜象，挂载，重定向根目录


海思3516学习blog，构建rootfs等
https://blog.csdn.net/qq_40334837/article/category/7504876
https://blog.csdn.net/u013308744/article/category/2615271

---

Linux下的Union文件系统 SquashFS只读部分镜象+可读写部分的层次叠加文件系统
https://fadeer.github.io/%E5%B7%A5%E4%BD%9C/2015/08/07/linux-union-filesystem.html

---

iw工具
https://mirrors.edge.kernel.org/pub/software/network/iw/

依赖libnl
https://www.infradead.org/~tgr/libnl/

参考
https://blog.csdn.net/qq_21792169/article/details/51224777

