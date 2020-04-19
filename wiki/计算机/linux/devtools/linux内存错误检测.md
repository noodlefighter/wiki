

---

## mtrace

<http://man7.org/linux/man-pages/man3/mtrace.3.html>

```
#include <mcheck.h>
```

程序中包含头文件, 使用mtrace命令行工具即可分析内存泄漏问题。

## Electric Fence (eFence)

> via: https://en.wikipedia.org/wiki/Electric_Fence
>
> Electric Fence is intended to find two common types of programming bugs:
>
> * Overrunning the end (or beginning) of a dynamically allocated buffer
> * Using a dynamically allocated buffer after returning it to the heap

用于检测动态分配内存（堆内存）的越界操作、释放后仍然写入的行为。原理是不释放堆内存，持续监控。

如果用的是archlinux，AUR里有包：`yay -S electricfence`即可安装好，查看手册`man libefence`。

用法：静态链接`libefence.a`即可，`-l:libefence.a`和`-lefence`都可以。



