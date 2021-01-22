---

## RTOS

### Android

大名鼎鼎的Android，其中Linux内核部分有很多能参考的。

https://android.googlesource.com/kernel/

https://source.android.com/setup/build/building-kernels

### ChibiOS [GPL 商业免费/收费]

http://www.chibios.org/

一个可GPL免费使用的RTOS 

带有一个apache开源协议的硬件抽象层

### Zephyr [Apache]

https://www.zephyrproject.org/

linux基金会下 因特尔主导的一个小巧的RTOS

有自己的硬件抽象层 主要针对小型系统

区别于大多数小RTOS的精简核心，zephyr更像一个小的linux，开发模式决定了模块间比较强的耦合。

### RT-Thread

https://github.com/RT-Thread/rt-thread

国产RTOS

### Mark3 [BSD]

http://www.mark3os.com

（已死，做个标记）

C++ RTOS

### TNKernel [不明]

https://bitbucket.org/dfrank/tneokernel

一个RTOS核 作者写了篇日志..码着看

http://dmitryfrank.com/articles/how_i_ended_up_writing_my_own_kernel



## 硬件抽象层

### libopencm3 [GPL3]

https://github.com/libopencm3/libopencm3

针对Cortex-M3的硬件抽象库

### ChibiOS HAL

http://www.chibios.org/dokuwiki/doku.php?id=chibios:product:hal:start

ChibiOS的硬件抽象层



## 编程框架

### protothread协程

PT协程，用得最多

### lw_coroutine协程

https://github.com/xiaoliang314/lw_coroutine
宣称比PT协程更高效更好用的类PT协程

### Async.h

https://github.com/naasking/async.h

asynchronous, stackless subroutines

### coroutine

https://github.com/cloudwu/coroutine

云风写的小协程库，强调非对称协程（和lua和python协程类似），其实PT也能实现一样的效果

### QP-nano

https://www.state-machine.com/qpn/

QP层次状态机框架Nano版。


## bootloader

### mcuboot

https://github.com/JuulLabs-OSS/mcuboot

## Runtime

### ShadowNode

嵌入式设备用的，小内存版本Node.js

[ShadowNode](https://github.com/yodaos-project/ShadowNode)

