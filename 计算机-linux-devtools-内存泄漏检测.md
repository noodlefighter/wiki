title: 内存泄漏检测
date: 2019-06-08
categories:
- 计算机
- linux
- devtools




---



## mtrace

<http://man7.org/linux/man-pages/man3/mtrace.3.html>

```
#include <mcheck.h>
```

程序中包含头文件, 使用mtrace命令行工具即可分析内存泄漏问题.

其实是对malloc/free的hook.