

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