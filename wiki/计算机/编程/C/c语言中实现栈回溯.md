# c语言中实现栈回溯



## libunwind库实现栈回溯



CMakeLists.txt使用libunwind库

```
pkg_check_modules(UNWIND libunwind-generic)
target_include_directories(gdmain-iot PUBLIC ${UNWIND_INCLUDE_DIRS})
target_link_libraries(gdmain-iot PUBLIC ${UNWIND_LIBRARIES})
```

异常时栈回溯：

```
#include <signal.h>
#include <libunwind.h>
#include <cxxabi.h>

void sigsegv_handler(int sig, siginfo_t *info, void *secret)
{
  // show backtrace
  unw_cursor_t cursor; unw_context_t uc;
  unw_word_t ip, sp;
  unw_getcontext(&uc);
  unw_init_local(&cursor, &uc);
  while (unw_step(&cursor) > 0) {
    unw_word_t  offset, pc;
    char fname[64];
    fname[0] = '\0';
    unw_get_reg(&cursor, UNW_REG_IP, &pc);
    (void) unw_get_proc_name(&cursor, fname, sizeof(fname), &offset);
    C_LOG("%p: (%s+0x%x) [%s]", pc, fname, offset, abi::__cxa_demangle(fname, NULL, NULL, NULL));
  }

  struct sigaction act;
  sigemptyset(&act.sa_mask);
  act.sa_flags = SA_NODEFER | SA_ONSTACK | SA_RESETHAND;
  act.sa_handler = SIG_DFL;
  sigaction(sig, &act, NULL);
  kill(getpid(),sig);
}

BOOL CGameApplication::init(event_base* evbase){
  struct sigaction act;
  sigemptyset(&act.sa_mask);
  act.sa_flags = SA_NODEFER | SA_ONSTACK | SA_RESETHAND | SA_SIGINFO;
  act.sa_sigaction = sigsegv_handler;
  sigaction(SIGSEGV, &act, NULL);
  return TRUE;
}

void CGameApplication::run(){
    *((uint8_t*)(0x0)) = 1; // segv error test
}

```

发现以上的代码，在Linux x86下正常，但在一块ARM无法正常打印
查资料得知，ARM的栈回溯需要.ARM.exidx、.ARM.extab两个段，readelf -u可以打印这些信息：

```
$ readelf -u test

Unwind table index '.ARM.exidx' at offset 0x5c0 contains 3 entries:

0x103f0 <_start>: 0x1 [cantunwind]

0x10518 <main>: @0x105b4
  Compact model index: 1
  0x9b      vsp = r11
  0x40      vsp = vsp - 4
  0x84 0x80 pop {r11, r14}
  0xb0      finish
  0xb0      finish

0x10538 <__libc_csu_init>: 0x1 [cantunwind]

```

看生成出来的ELF确实是有这些信息的，但打印依旧不正常，当前libunwind版本1.1，尝试升级到1.6.2，待测试是否成功（TODO:待测试）。
