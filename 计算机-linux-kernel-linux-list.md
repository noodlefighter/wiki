title: linux-list
date: 2019-06-12
categories:
- 计算机
- linux
- kernel




---

`#include <linux/list.h>`

## linux内核list数据结构用法

>  via: https://notes.shichao.io/lkd/ch6/#the-linux-kernels-implementation



> TODO:

## 别人移植好的, 用户态下能用的linux的list.h

<https://github.com/Akagi201/list/blob/master/list.h>

> Here is a recipe to cook list.h for user space program.
> 1. copy list.h from linux/include/list.h
> 2. remove
>     - #ifdef __KERNE__ and its #endif
>     - all #include line
>     - prefetch() and rcu related functions
> 3. add macro offsetof() and container_of

