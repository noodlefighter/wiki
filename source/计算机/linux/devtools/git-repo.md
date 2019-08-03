

---



使用

## repo工具

git-repo是google为了android项目做的系统级构建管理工具，android项目由大量git仓库构成，而git自身的subtree和submodule不足以作为支撑。

大概思路是：

* 用一个xml文件描述构建目标，包含git仓库的地址、分支信息，并和目录结构挂钩；

* 把这个repo的xml也放在git仓库里，以实现构建的版本管理；
* 做一个命令行工具repo，只需要输入一条命令即可完成所有仓库的检出。



## repo使用

执行repo时，会对自身进行更新，国内网络有问题