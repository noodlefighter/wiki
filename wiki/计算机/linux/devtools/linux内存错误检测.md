

---

## Linux Core Dump 内核转储


```
# ulimit -c unlimited
```

开启后，程序执行崩溃后会在当前目录下保存core：

```
Segmentation fault (core dumped)
# ls
core 
```

修改coredump保存目录：

```
# echo "/root/nfsroot/sk02/ebi_works/core-%p-%t" > /proc/sys/kernel/core_pattern
```

gdb调试coredump文件：

```
$ gdb ./test core-test-31421-1476266571
```



## mtrace

mtrace是glibc自带的工具

<http://man7.org/linux/man-pages/man3/mtrace.3.html>

```
#include <mcheck.h>
```

程序中包含头文件, 使用mtrace命令行工具即可分析内存泄漏问题。



## dmalloc

也是类似mtarce的工具，要求将库链接到被调试的程序中。

```
The debug memory allocation or dmalloc library has been designed as a drop in replacement for the system's malloc, realloc, calloc, free and other memory management routines while providing powerful debugging facilities configurable at runtime. These facilities include such things as memory-leak tracking, fence-post write detection, file/line number reporting, and general logging of statistics.
```

https://dmalloc.com/

使用指南： https://stuff.mit.edu/afs/sipb/project/gnucash-test/src/dmalloc-4.8.2/dmalloc.html

基本用法：

1. 安装dmalloc后，得到实用程序dmalloc和静态库libdmalloc.a(适用与单线程程序)和libdmallocth.a(多线程程序)

2. 程序中插入包含，在其他的头文件的后面：

   ```c
   #ifdef DMALLOC
   #include "dmalloc.h"
   #endif
   ```

   编译：

   ```
   $ gcc -DDMALLOC -DDMALLOC_FUNC_CHECK -l:libdmallocth.a test.c
   ```

   如果不包含`dmalloc.h`直接链上，则日志中不会提供源文件名、行号等信息。

3. shell中执行：

   ```
   $ function dmalloc { eval `command dmalloc -b $*`; }
   $ dmalloc -l logfile -i 5 low
   $ ./test
   ```

   当前目录下的`logfile`即是dmalloc的日志了

若日志中出现类似`98237: 1171: WARNING: tried to free(0) from 'ra=0xb6f394cc'`，参考用户手册[3.9.4 Translating Return Addresses into Code Locations](https://dmalloc.com/docs/latest/online/dmalloc_17.html#SEC23)，使用gdb可以找到源码位置：

```
# you may need to add the following commands to load in shared libraries
(gdb) sharedlibrary
(gdb) add-shared-symbol-files

(gdb) x 0x10234d
0x10234d <_findbuf+132>: 0x7fffceb7

(gdb) info line *(0x82cc)
Line 1092 of argv.c starts at pc 0x7540 and ends at 0x7550.
```




## Electric Fence (eFence)

> via: https://en.wikipedia.org/wiki/Electric_Fence
>
> Electric Fence is intended to find two common types of programming bugs:
>
> * Overrunning the end (or beginning) of a dynamically allocated buffer
> * Using a dynamically allocated buffer after returning it to the heap

用于检测动态分配内存（堆内存）的越界操作、释放后仍然写入的行为。原理是不释放堆内存，持续监控。

如果用的是archlinux，AUR里有包：`yay -S electricfence`即可安装好，查看手册`man libefence`。

```
INSTRUCTIONS FOR DEBUGGING YOUR PROGRAM
       1. Link with libefence.a as explained above.
       2. Run your program in a debugger and fix any overruns or accesses to free memory.
       3. Quit the debugger.
       4. Set EF_PROTECT_BELOW = 1 in the shell environment.
       5. Repeat step 2, this time repairing underruns if they occur.
       6. Quit the debugger.
       7. Read the restrictions in the section on WORD-ALIGNMENT AND OVERRUN DETECTION.  See if you can set EF_ALIGNMENT to 0 and repeat step 2. Sometimes this will be too much work, or there will be problems with library routines for which you don't have the source, that will prevent you from doing this.
```

用法：

1. 静态链接`libefence.a`，如`-l:libefence.a`
2. 使用debugger，默认行为是efence会捕获出问题的地方，然后退出
3. 设置环境变量`EF_PROTECT_BELOW=1`，把行为修改成出问题时SIGSEGV，从而使debugger能捕获到错误



