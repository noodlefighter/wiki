

---



## 传统方式编译

参考：

https://wiki.ubuntu.com/Kernel/BuildYourOwnKernel

https://wiki.archlinux.org/index.php/Kernel/Traditional_compilation



大致是：

* 去`https://www.kernel.org/pub/linux/kernel`拖内核
* 根据发行版的说明打补丁
* 修改配置
* `make`，`make modules_install`、`make install `
* 文档里说最好把内核头文件先安装了，因为一些驱动编译可能会用到，但



Tips:

* `make localmodconfig`可以自动根据本地情况生成极简配置，但通用性很差，而已可能不支持一些新硬件
* Arch里用`zcat /proc/config.gz > .config`可将当前配置导出
* 直接`make menuconfig`可以，不知道用配置

