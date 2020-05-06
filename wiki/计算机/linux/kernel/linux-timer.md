


# linux 内核中各delay函数的区别


via: https://www.kernel.org/doc/html/latest/timers/timers-howto.html

**ATOMIC CONTEXT:**

You must use the *delay family of functions.

**NON-ATOMIC CONTEXT:**

You should use the *sleep[_range] family of functions.

– Backed by busy-wait loop（**< ~10us**）:

> udelay(unsigned long usecs)

– Backed by hrtimers（**10us - 20ms**）:

> usleep_range(unsigned long min, unsigned long max)

– Backed by jiffies / legacy_timers（**10ms+** ）：

> msleep(unsigned long msecs) msleep_interruptible(unsigned long msecs)



## Linux内核中的高精度时钟（HRTIMER，High Resolution Timers）

`CONFIG_HIGH_RES_TIMERS`，在Kconfig的`General setup/Timers subsystem/High Resolution Timer Support`中。



