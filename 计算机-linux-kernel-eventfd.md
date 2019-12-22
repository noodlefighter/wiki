title: eventfd
date: 2019-06-16
categories:
- 计算机
- linux
- kernel




---

实际上就是linux kernel中通过eventfd()打开一个内核对象, 发送/接收双方通过read/write实现异步通知.

>  via: <https://linux.die.net/man/2/eventfd>
>
> **Description**
>
> **eventfd**() creates an "eventfd object" that can be used as an event wait/notify mechanism by user-space applications, and by the kernel to notify user-space applications of events. The object contains an unsigned 64-bit integer (*uint64_t*) counter that is maintained by the kernel. This counter is initialized with the value specified in the argument *initval*.

其实就是内核对象中维护着uint64_t计数值, 默认情况下 `write()`的值会加在计数值上, 而`read()`会读出计数值并清零计数值.

一般用法就是: 接收方打开文件fd, 发送方写1来进行通知.

但也有flags中设置`EFD_SEMAPHORE`的用法, `write()`每次只能写入1, `read()`每次只能读出1, 行为就像多线程旗语中的信号量.

