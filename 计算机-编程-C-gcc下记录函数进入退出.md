title: gcc下记录函数进入退出
date: 2019-07-16
categories:
- 计算机
- 编程
- C




---



参考：

https://gcc.gnu.org/onlinedocs/gcc-4.5.1/gcc/Code-Gen-Options.html#index-finstrument_002dfunctions-2114

https://mcuoneclipse.com/2015/04/04/poor-mans-trace-free-of-charge-function-entryexit-trace-with-gnu-tools/

http://michael.hinespot.com/tutorials/gcc_trace_functions

## 加入`-finstrument-functions`后发生段错误的问题

定位到调用`__cyg_profile_func_enter` 时发生segmentation error，发现调用了，加入参数排除掉实现这函数的源文件即可：

```
-finstrument-functions-exclude-file-list=trace.c
```

或者给符号加`__attribute__ ((no_instrument_function))`也能解决。

## Trace and profile function calls with GCC

> via:https://balau82.wordpress.com/2010/10/06/trace-and-profile-function-calls-with-gcc/

Software debugging is a complex task. There is always the need to collect all available information, in order to detect and understand the problem fast and to think of a proper solution. Sometimes it’s more convenient to debug step-by-step, sometimes it’s better to make the program run completely, and then trace the execution flow “offline”.

Another important step in software development is profiling. GNU offers “`gprof`” as a tool to analyze the execution time of functions. The [working principle](http://www.delorie.com/gnu/docs/binutils/gprof_25.html) of `gprof` is that it polls the program state with a small sampling interval and notes the function that is executing. In this case small functions could also not appear in the profiling data because their execution time is smaller than an interval.

I recently tried to use a feature of GNU GCC that can be of some help both for tracing and for profiling. It’s the following option (from [its GNU GCC Manual section](http://gcc.gnu.org/onlinedocs/gcc-4.5.1/gcc/Code-Gen-Options.html#index-finstrument_002dfunctions-2114)):

> - `-finstrument-functions`
>
>   Generate instrumentation calls for entry and exit to functions. Just after function entry and just before function exit, the following profiling functions will be called with the address of the current function and its call site.
>
>   void __cyg_profile_func_enter (void *this_fn, void *call_site);
>
>   __void __cyg_profile_func_exit  (void *this_fn, void *call_site);

The execution flow can be traced implementing these monitoring points, for example writing on file some useful information.

Suppose you have to analyze the following code:

```c
#include <stdio.h>

void foo() {
 printf("foo\n");
}

int main() {

 foo();

 return 0;
}

```

Create a file called “`trace.c`” with the following content:

```c
#include <stdio.h>
#include <time.h>

static FILE *fp_trace;

void
__attribute__ ((constructor))
trace_begin (void)
{
 fp_trace = fopen("trace.out", "w");
}

void
__attribute__ ((destructor))
trace_end (void)
{
 if(fp_trace != NULL) {
 fclose(fp_trace);
 }
}

void
__cyg_profile_func_enter (void *func,  void *caller)
{
 if(fp_trace != NULL) {
 fprintf(fp_trace, "e %p %p %lu\n", func, caller, time(NULL) );
 }
}

void
__cyg_profile_func_exit (void *func, void *caller)
{
 if(fp_trace != NULL) {
 fprintf(fp_trace, "x %p %p %lu\n", func, caller, time(NULL));
 }
}
```

The idea is to write into a log (in our case “`trace.out`“) the function addresses, the address of the call and the execution time. To do so, a file needs to be open at the beginning of execution. The GCC-specific attribute “[`constructor`](http://gcc.gnu.org/onlinedocs/gcc-4.5.1/gcc/Function-Attributes.html#index-g_t_0040code_007bconstructor_007d-function-attribute-2343)” helps in defining a function that is executed before “main”. In the same way the attribute “`destructor`” specifies that a function must be executed when the program is going to exit.

To compile and execute the program, the command-line is:

```bash
$ gcc -finstrument-functions -g -c -o main.o main.c
$ gcc -c -o trace.o trace.c
$ gcc main.o trace.o -o main
$ ./main
foo
$ cat trace.out
e 0x400679 0x394281c40b 1286372153
e 0x400648 0x40069a 1286372153
x 0x400648 0x40069a 1286372153
x 0x400679 0x394281c40b 1286372153
```

To understand the addresses, the “`addr2line`” tool can be used: it’s a tool included in “`binutils`” package that, given an executable with debug information, maps an execution address to a source code file and line. I put together an executable shell script (“`readtracelog.sh`“) that uses `addr2line` to print the trace log into a readable format:

```bash
#!/bin/sh
if test ! -f "$1"
then
 echo "Error: executable $1 does not exist."
 exit 1
fi
if test ! -f "$2"
then
 echo "Error: trace log $2 does not exist."
 exit 1
fi
EXECUTABLE="$1"
TRACELOG="$2"
while read LINETYPE FADDR CADDR CTIME; do
 FNAME="$(addr2line -f -e ${EXECUTABLE} ${FADDR}|head -1)"
 CDATE="$(date -Iseconds -d @${CTIME})"
 if test "${LINETYPE}" = "e"
 then
 CNAME="$(addr2line -f -e ${EXECUTABLE} ${CADDR}|head -1)"
 CLINE="$(addr2line -s -e ${EXECUTABLE} ${CADDR})"
 echo "Enter ${FNAME} at ${CDATE}, called from ${CNAME} (${CLINE})"
 fi
 if test "${LINETYPE}" = "x"
 then
 echo "Exit  ${FNAME} at ${CDATE}"
 fi
done < "${TRACELOG}"
```

Testing the script with the previous output, the result is:

```bash
$ ./readtracelog.sh main trace.out
Enter main at 2010-10-06T15:35:53+0200, called from ?? (??:0)
Enter foo at 2010-10-06T15:35:53+0200, called from main (main.c:9)
Exit  foo at 2010-10-06T15:35:53+0200
Exit  main at 2010-10-06T15:35:53+0200
```

The “`??`” symbol indicates that `addr2line` has no debug information on that address: in fact it should belong to C runtime libraries that initialize the program and call the main function. In this case the execution time was very small (less than a second) but in more complex scenarios the execution time can be useful to detect where the application spends the most time. It is also a good idea to use the most precise timer on the system, such as [gettimeofday](http://linux.die.net/man/2/gettimeofday) in Linux that returns also fractions of a second.

Some thoughts for embedded platforms:

- It is possible to have fine-grain timing information if the platform contains an internal hardware timer, counting even single clock cycles. It will become then important to reduce the overhead of the entry and exit functions to measure the real function execution time.
- The trace information can be sent to the serial port (for example in binary form), and then interpreted by a program running on PC.
- The entry and exit functions can be used to monitor also the state of other hardware peripherals, such as a temperature sensor.