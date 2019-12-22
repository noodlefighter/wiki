title: DKMS
date: 2019-06-08
categories:
- 计算机
- linux
- devtools




---



##  动态内核模块支持



> 来源: Wiki百科
>
> via: https://zh.wikipedia.org/wiki/%E5%8A%A8%E6%80%81%E5%86%85%E6%A0%B8%E6%A8%A1%E5%9D%97%E6%94%AF%E6%8C%81

动态内核模块支持(DKMS) 是用来生成Linux的内核模块的一个框架，其源代码一般不在Linux内核源代码树。 当新的内核安装时，DKMS支持的内核设备驱动程序 到时会自动重建。 DKMS可以用在两个方向：如果一个新的内核版本安装，自动编译所有的模块，或安装新的模块（驱动程序）在现有的系统版本上，而不需要任何的手动编译或预编译软件包需要。例如，这使得新的显卡可以使用在旧的Linux系统上。

DKMS是由戴尔的Linux工程团队在2003年写的。它已经被许多Linux发行版所包含，如Ubuntu 8.10和Fedora。它是以GNU通用公共许可证（GPL）v2或以后的条款发布下的免费软件。DKMS原生支持RPM和DEB软件包格式。

DKMS（Dynamic Kernel Module Support）动态内核模块支持。 旨在创建一个内核相关模块源可驻留的框架，以便在升级内核时可以很容易地重建模块。这将允许 Linux 供应商提供较低版本的驱动程序，而无需等待新内核版本发行，同时还可以省去尝试重新编译新内核模块的客户预期要完成的工作。Oikawa等人在1996年提出一种与LKM类似的动态核心模块（DKMs）技术。与LKM一样，DKMs以文件的形式存储并能在系统运行过程中动态地加载和卸载。DKMs由一个用户层的DKM服务器来管理，并非由内核来管理。当核心需要某模块时，由DKM服务器负责把相应的DKM加载；当核心的内存资源紧缺时，由DKM服务器负责卸载一个没有被使用的DKM。缺点是所有的DKM是存储在本地系统上的，占用了大量宝贵的存储空间。



## 实现

github仓库: <https://github.com/dell/dkms>



## Archlinux对它的支持

> via: https://wiki.archlinux.org/index.php/Dynamic_Kernel_Module_Support

### 列出内核模块

列出当前模块的状态，版本，包括源码树内的模块：

```
# dkms status
```

### 重新构建模块

为当前内核重新构建所有的模块：

```
# dkms autoinstall -k
```

或者重新构建某个特定的模块：

```
# dkms autoinstall -k 3.16.4-1-ARCH
```