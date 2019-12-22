title: popen
date: 2019-07-09
categories:
- 计算机
- 编程
- C




---



## 介绍

> via: https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.3.0/com.ibm.zos.v2r3.bpxbd00/rpopen.htm

### 原型

```c
#include <stdio.h>
FILE *popen(const char *command, const char *mode);
int pclose(FILE *stream);
```

### 一般性描述

popen（）函数执行string命令指定的命令。它在调用程序和执行的命令之间创建一个管道，并返回一个指向流的指针，该流可用于读取或写入管道。

执行命令的环境就像使用fork（）在popen（）调用中创建子进程一样，并且子进程调用了sh实用程序：

```c
execl("/bin/sh", "sh", "-c", command, (char *)0);
```

popen（）函数确保在子进程中关闭在父进程中保持打开的先前popen（）调用的任何流。

popen（）的mode参数是一个指定I / O模式的字符串： 

1. 如果mode为r，则文件描述符STDOUT_FILENO将在子进程启动时成为管道的可写端。调用进程中的文件描述符fileno（stream），其中stream是popen（）返回的流指针，将是管道的可读端。 
2. 如果mode是w，则文件描述符STDIN_FILENO将在子进程启动时成为管道的可读端。调用进程中的文件描述符fileno（stream），其中stream是popen（）返回的流指针，将是管道的可写端。 
3. 如果mode是任何其他值，则返回NULL指针，并将errno设置为EINVAL。

在popen（）之后，父进程和子进程都能够在终止之前独立执行。

由于共享打开文件，因此模式r命令可用作输入过滤器，模式w命令可用作输出过滤器。

在打开输入过滤器之前（即，在popen（）之前）进行缓冲读取可能会使该过滤器的标准输入位置错误。使用fflush（）缓冲区刷新可以防止输出滤波器出现类似问题。

用popen（）打开的流应该由pclose（）关闭。

popen（）的行为是针对r和w的模式的值指定的。支持rb和wb的模式值，但不可移植。

如果无法执行shell命令，则pclose（）返回的子终止状态就像使用exit（127）或_exit（127）终止shell命令一样。

如果应用程序使用pid参数大于0调用waitpid（），并且它仍然具有使用popen（）打开创建的流，则必须确保pid不引用popen（）启动的进程

popen（）返回的流将被指定为面向字节的。

文件标记和转换的特殊行为：当指定FILETAG（，AUTOTAG）运行时选项时，由popen（）打开的父进程和子进程之间的通信管道将在第一个I /上用编写器的程序CCSID标记O.例如，如果指定了popen（some_command，“r”），那么popen（）返回的流将在子进程的程序CCSID中标记。


### 返回值

如果成功，popen（）返回一个指向打开流的指针，该指针可用于读取或写入管道。

如果不成功，popen（）返回NULL指针并将errno设置为以下值之一：
EINVAL：The mode argument is invalid.

popen() may also set errno values as described by spawn(), fork(), or pipe().



## pclose

通过`pclose()`获取执行结果（需要`#include <sys/wait.h>`）：

````
rv = pclose(pp);
printf("ifexited: %d\n", WIFEXITED(rv));
if (WIFEXITED(rv)) {  
	printf("subprocess exited, exit code: %d\n", WEXITSTATUS(rv));
}
````



## 一例：popen获取系统命令的输出内容



```
fp = popen("top -n 1", "r");
if(NULL != fp) {
    fgets(topline[0], 256, fp);
    fgets(topline[1], 256, fp);
	pclose(fp);
} else {
    printf("command failed!\n");
}

```



