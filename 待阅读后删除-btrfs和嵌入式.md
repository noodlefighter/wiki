title: btrfs和嵌入式
date: 2019-06-09
categories:
- 待阅读后删除




---

 btrfs是嵌入式Linux的真正好朋友。

可能很多旁友还没有意识到这一点，我来展开讲一下。

设想uboot支持btrfs，包括subvolume，它可以从一个叫做boot的subvolume找到最初的boot.scr，这个script可以根据一些标记文件确定该从哪个subvol的/boot目录里载入kernel，initramfs和dtb，并正确的设置cmdline，使用这个subvol作为rootfs。这是策略一。

策略二是用于载入kernel等启动文件的subvol是一个只读的，kernel起来之后利用initramfs或者截获/sbin/init，立即从这个只读的subvol创建一个可写的subvolume副本，用这个副本作为rootfs启动系统，这样rootfs是可写的，同时每次重启所有的修改都挥发掉。兼顾了只读的健壮和linux hfs的读写要求。

比策略三更强的做法可以是每次reboot时前一次的读写subvol不必立即删除，可以维护一个列表这样每次启动对文件系统的修改以及log都在，非常有助于分析系统。

最后相信你也看出来了，用这种策略做a/b升级和recovery简直不要太爽。

那么我们最后说它和现在的嵌入式linux或者Android的最重要区别在哪里呢？

就是抹去了所有分区之间的界限，这也是raid或btrfs这类系统的最初设计目标之一，术语上叫做pooling。虽然这不是在跨硬件介质的pooling，但是能够在一个卷上把所有系统镜像，升级要求，启动分区乃至用户数据都装下，不但可以利用snapshot管理系统，还可以用它管理应用程序（想想Ubuntu的snap）。刚真，这就是文件系统的真正未来，还具有绝佳的可扩展能力。

Android开发者曾经研究过btrfs，最终没有选做Android的rootfs是当时btrfs只有开放的加密接口但并没有一个solid的实现，于是谷歌就暂时没有选择btrfs。绝对堪称傻叉了。
 