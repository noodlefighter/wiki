

# valgrind工具包



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

