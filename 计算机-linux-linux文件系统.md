title: linux文件系统
date: 2019-08-18
categories:
- 计算机
- linux




---





------

Linux下的Union文件系统 SquashFS只读部分镜象+可读写部分的层次叠加文件系统
https://fadeer.github.io/%E5%B7%A5%E4%BD%9C/2015/08/07/linux-union-filesystem.html

## linux文件系统Overlayfs机制

Overlayfs = Overlay filesystem.

linux在文件系统上

> arch的wiki: 
>
> <https://wiki.archlinux.org/index.php/Overlay_filesystem>
>
> kernel的git commit: <https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=e9be9d5e76e34872f0c37d72e25bc27fe9e2c54c>

Overlayfs允许一个通常是读写的目录树 覆盖到另一个只读目录树上。所有的修改会在上面的可写层。这样的机制最常用于Live CD，但还有很多其他用途。

该实现与其他“union filesystem”实现的不同之处在于，在打开文件之后，所有操作都直接进入底层的lower层或upper层文件系统。这简化了实现，并在这些情况下允许本机性能。 Overlayfs在出现在linux内核3.18之后。



## linux下mount ntfs分区只读的问题

写入文件提示read only，需要安装`ntfs-3g`包才能获得完整的读写支持。



## SquashFS

HowTo:

https://www.tldp.org/HOWTO/html_single/SquashFS-HOWTO/

Format:

https://dr-emann.github.io/squashfs/#superblock

