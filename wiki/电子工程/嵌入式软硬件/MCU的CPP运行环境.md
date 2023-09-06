## MCU下的C++运行环境



ChatGPT给的回答：

```
除了像C语言一样需要stack、bss数据清零、data段复制到RAM中外，C++还需要完成以下几个步骤：
- 构造全局对象：C++程序中的全局变量和静态变量需要在程序启动时被构造，这一过程需要在C++启动代码中完成。
- 构造函数调用：C++中的类对象都有构造函数，需要在对象创建时被调用。这一过程需要在程序启动时完成。
- 虚函数表初始化：如果C++程序中使用了虚函数，需要将虚函数表进行初始化，以便在程序运行时能够正确地调用虚函数。
- RTTI初始化：如果C++程序中使用了RTTI（Run-time Type Information），需要进行RTTI的初始化。
- 异常处理：C++程序中使用了异常处理机制，需要在程序启动时初始化异常处理机制。
```



> 一段C++启动代码
>
> via:  https://allthingsembedded.com/post/2019-01-03-arm-cortex-m-startup-code-for-c-and-c/

```
#include <algorithm>
#include <cstdint>
#include "core_cm7.h"

static void BoardInitialization() {
    SCB->CPACR |= ((3UL << 10*2)|(3UL << 11*2));  /* set CP10 and CP11 Full Access */
}

extern "C"
void ResetHandler() {
    // Initialize data section
    extern std::uint8_t __data_start__;
    extern std::uint8_t __data_end__;
    extern std::uint8_t __etext;
    std::size_t size = static_cast<size_t>(&__data_end__ - &__data_start__);
    std::copy(&__etext, &__etext + size, &__data_start__);

    // Initialize bss section
    extern std::uint8_t __bss_start__;
    extern std::uint8_t __bss_end__;
    std::fill(&__bss_start__, &__bss_end__, UINT8_C(0x00));

    // Initialize static objects by calling their constructors
    typedef void (*function_t)();
    extern function_t __init_array_start;
    extern function_t __init_array_end;
    std::for_each(&__init_array_start, &__init_array_end, [](const function_t pfn) {
        pfn();
    });

    BoardInitialization();

    // Jump to main
    asm ("bl main");
}
```

初始化全局静态对象即添加代码段：

```
  // 启动文件C++环境缺失，初始化静态全局对象
  typedef void (*function_t)();
  extern function_t __init_array_start;
  extern function_t __init_array_end;
  std::for_each(&__init_array_start, &__init_array_end, [](const function_t pfn) {
      pfn();
  });
```

