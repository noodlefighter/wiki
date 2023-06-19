

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

一个用于检测堆内存越界读写、释放后仍然写入等错误。简单使用方法：

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


参考（manual：https://linux.die.net/man/3/efence），启动时可设置的环境变量控制efence行为：

- `EF_ALIGNMENT`：内存地址对齐
- `EF_PROTECT_BELOW`：检查内存操作越界的情况，在内存块尾部添加不可访问区域
- `EF_PROTECT_FREE`：检查内存被释放后依旧被操作的情况，原理是free()后将地址设置不可访问，且永不重新分配
- `EF_ALLOW_MALLOC_0`：允许malloc(0)，默认不允许
- `EF_FILL`设置申请到的内存的初始值，用于检测变量未初始化等情况

注意：

- 这工具还是太老了，实际用起来各种问题，试用后发现fedora的那些patch比ubuntu的好使，我自己fork了一份方便修改维护，用的时候应该直接源码编译安装，方便调试 https://github.com/noodlefighter/electric-fence
- 如果遇到`mprotect() failed: No Memory`，其实是mmap数量受限制，`echo 1280000 > /proc/sys/vm/max_map_count`可解决（mmap情况：`cat /proc/$pid/maps`）



## valgrind工具包（包含memcheck）

[memcheck的文档](http://valgrind.org/docs/manual/mc-manual.html)

使用未初始化的内存 (Use of uninitialised memory)

使用已经释放了的内存 (Reading/writing memory after it has been free’d)

使用超过 malloc分配的内存空间(Reading/writing off the end of malloc’d blocks)

对堆栈的非法访问 (Reading/writing inappropriate areas on the stack)

申请的空间是否有释放 (Memory leaks – where pointers to malloc’d blocks are lost forever)

malloc/free/new/delete申请和释放内存的匹配(Mismatched use of malloc/new/new [] vs free/delete/delete [])

src和dst的重叠(Overlapping src and dst pointers in memcpy() and related functions)


```
用法: valgrind [options] prog-and-args
[options]: 常用选项，适用于所有Valgrind工具

    -tool=<name> 最常用的选项。运行 valgrind中名为toolname的工具。默认memcheck。

        memcheck ------> 这是valgrind应用最广泛的工具，一个重量级的内存检查器，能够发现开发中绝大多数内存错误使用情况，比如：使用未初始化的内存，使用已经释放了的内存，内存访问越界等。

        callgrind ------> 它主要用来检查程序中函数调用过程中出现的问题。

        cachegrind ------> 它主要用来检查程序中缓存使用出现的问题。

        helgrind ------> 它主要用来检查多线程程序中出现的竞争问题。

        massif ------> 它主要用来检查程序中堆栈使用中出现的问题。

        extension ------> 可以利用core提供的功能，自己编写特定的内存调试工具
```

特点:

- 无需重新编译程序
- 缺点是很慢，“valgrind模拟的一个软CPU，将可执行程序运行在其中”、“valgrind的是单线程的（应该是），它会将你程序的所有线程统一管理起来”



测试当前环境是否能正常使用valgrind，测试`ls -l`命令是否有内存泄漏：

```
$ valgrind --tool=memcheck --leak-check=yes  ls -l
```



问题集：

- `valgrind: Fatal error at startup: a function redirection`：glibc没有debuginfo



## 重写C的malloc

> https://www.gnu.org/software/libc/manual/html_node/Replacing-malloc.html
>
> The minimum set of functions which has to be provided by a custom `malloc` is given in the table below.
>
> - `malloc`
> - `free`
> - `calloc`
> - `realloc`
>
> These `malloc`-related functions are required for the GNU C Library to work.[1](https://www.gnu.org/software/libc/manual/html_node/Replacing-malloc.html#FOOT1)
>
> The `malloc` implementation in the GNU C Library provides additional functionality not used by the library itself, but which is often used by other system libraries and applications. A general-purpose replacement `malloc` implementation should provide definitions of these functions, too. Their names are listed in the following table.
>
> - `aligned_alloc`
> - `malloc_usable_size`
> - `memalign`
> - `posix_memalign`
> - `pvalloc`
> - `valloc`



## C++中使用这些内存检查工具

>  https://gcc.gnu.org/onlinedocs/libstdc++/manual/memory.html
>
> ##### Disabling Memory Caching
>
> In use, `allocator` may allocate and deallocate using implementation-specific strategies and heuristics. Because of this, a given call to an allocator object's `allocate` member function may not actually call the global `operator new` and a given call to to the `deallocate` member function may not call `operator delete`.
>
> This can be confusing.
>
> In particular, this can make debugging memory errors more difficult, especially when using third-party tools like valgrind or debug versions of `new`.
>
> There are various ways to solve this problem. One would be to use a custom allocator that just called operators `new` and `delete` directly, for every allocation. (See the default allocator, `include/ext/new_allocator.h`, for instance.) However, that option may involve changing source code to use a non-default allocator. Another option is to force the default allocator to remove caching and pools, and to directly allocate with every call of `allocate` and directly deallocate with every call of `deallocate`, regardless of efficiency. As it turns out, this last option is also available.
>
> To globally disable memory caching within the library for some of the optional non-default allocators, merely set `GLIBCXX_FORCE_NEW` (with any value) in the system's environment before running the program. If your program crashes with `GLIBCXX_FORCE_NEW` in the environment, it likely means that you linked against objects built against the older library (objects which might still using the cached allocations...).



> C++重写new和delete，比想像中困难 https://www.cnblogs.com/coding-my-life/p/10125538.html
