

---



moreutils工具包中的errno工具，方便查看errno定义，而且是经过本地化的：

如`errno 5`:

```
EIO 5 输入/输出错误
```

`errno -l`：

```
EPERM 1 不允许的操作
ENOENT 2 没有那个文件或目录
ESRCH 3 没有那个进程
EINTR 4 被中断的系统调用
EIO 5 输入/输出错误
ENXIO 6 没有那个设备或地址
E2BIG 7 参数列表过长
ENOEXEC 8 可执行文件格式错误
EBADF 9 错误的文件描述符
ECHILD 10 没有子进程
EAGAIN 11 资源暂时不可用
ENOMEM 12 无法分配内存
EACCES 13 权限不够
EFAULT 14 错误的地址
ENOTBLK 15 需要块设备
EBUSY 16 设备或资源忙
EEXIST 17 文件已存在
EXDEV 18 无效的跨设备链接
ENODEV 19 没有那个设备
ENOTDIR 20 不是目录
EISDIR 21 是一个目录
EINVAL 22 无效的参数
ENFILE 23 系统中打开的文件过多
EMFILE 24 打开的文件过多
ENOTTY 25 对设备不适当的 ioctl 操作
ETXTBSY 26 文本文件忙
EFBIG 27 文件过大
ENOSPC 28 设备上没有空间
ESPIPE 29 非法 seek 操作
EROFS 30 只读文件系统
EMLINK 31 过多的链接
EPIPE 32 断开的管道
EDOM 33 数值参数超出域
ERANGE 34 数值结果超出范围
EDEADLK 35 已避免资源死锁
ENAMETOOLONG 36 文件名过长
ENOLCK 37 没有可用的锁
ENOSYS 38 函数未实现
ENOTEMPTY 39 目录非空
ELOOP 40 符号连接的层数过多
EWOULDBLOCK 11 资源暂时不可用
ENOMSG 42 没有符合需求格式的消息
EIDRM 43 标识符已删除
ECHRNG 44 通道编号超出范围
EL2NSYNC 45 级别 2 尚未同步
EL3HLT 46 级别 3 已关闭
EL3RST 47 级别 3 已重置
ELNRNG 48 链接数超出范围
EUNATCH 49 未加载协议驱动程序
ENOCSI 50 没有可用的 CSI 结构
EL2HLT 51 级别 2 己关闭
EBADE 52 无效的交换
EBADR 53 无效的请求描述符
EXFULL 54 交换满
ENOANO 55 没有 anode
EBADRQC 56 无效的请求码
EBADSLT 57 不适用的 slot
EDEADLOCK 35 已避免资源死锁
EBFONT 59 错误的字体文件格式
ENOSTR 60 设备不是流
ENODATA 61 没有可用的数据
ETIME 62 计时器超时
ENOSR 63 流资源不足
ENONET 64 机器不在网络中
ENOPKG 65 包未安装
EREMOTE 66 对象是远程的
ENOLINK 67 链接已有服务
EADV 68 通知错误
ESRMNT 69 Srmount 错误
ECOMM 70 发送时出现通讯错误
EPROTO 71 协议错误
EMULTIHOP 72 尝试 Multihop
EDOTDOT 73 RFS 特定错误
EBADMSG 74 错误的消息
EOVERFLOW 75 对已定义的数据类型来说值过大
ENOTUNIQ 76 网络上的名称不是唯一的
EBADFD 77 文件描述符处于错误状态
EREMCHG 78 远程地址已改变
ELIBACC 79 无法访问必须的共享库
ELIBBAD 80 正在访问一个已毁坏的共享库
ELIBSCN 81 a.out 中的 .lib 节已毁坏
ELIBMAX 82 试图与过多的共享库相链接
ELIBEXEC 83 无法直接执行共享库
EILSEQ 84 无效或不完整的多字节字符或宽字符
ERESTART 85 被中断的系统调用应该重新启动
ESTRPIPE 86 流管道错误
EUSERS 87 用户过多
ENOTSOCK 88 对非套接字进行套接字操作
EDESTADDRREQ 89 需要目标地址
EMSGSIZE 90 消息过长
EPROTOTYPE 91 错误的 socket 协议类型
ENOPROTOOPT 92 不可用的协议
EPROTONOSUPPORT 93 不支持的协议
ESOCKTNOSUPPORT 94 不支持的套接字类型
EOPNOTSUPP 95 不支持的操作
EPFNOSUPPORT 96 不支持的协议族
EAFNOSUPPORT 97 协议不支持的地址族
EADDRINUSE 98 地址已在使用
EADDRNOTAVAIL 99 无法指定被请求的地址
ENETDOWN 100 网络已关闭
ENETUNREACH 101 网络不可达
ENETRESET 102 重置时断开网络连接
ECONNABORTED 103 由软件导致的连接断开
ECONNRESET 104 连接被对方重设
ENOBUFS 105 没有可用的缓冲区空间
EISCONN 106 传输端点已连接
ENOTCONN 107 传输端点尚未连接
ESHUTDOWN 108 无法在传输端点关闭以后发送
ETOOMANYREFS 109 过多的引用：无法接合
ETIMEDOUT 110 连接超时
ECONNREFUSED 111 拒绝连接
EHOSTDOWN 112 主机关闭
EHOSTUNREACH 113 没有到主机的路由
EALREADY 114 操作已经在进行
EINPROGRESS 115 操作现在正在进行
ESTALE 116 过旧的文件控柄
EUCLEAN 117 结构需要清理
ENOTNAM 118 不是 XENIX 命名的类型文件
ENAVAIL 119 没有可用的 XENIX 信号量
EISNAM 120 是一个有名类型文件
EREMOTEIO 121 远程 I/O 错误
EDQUOT 122 超出磁盘限额
ENOMEDIUM 123 找不到介质
EMEDIUMTYPE 124 错误的介质类型
ECANCELED 125 操作已取消
ENOKEY 126 需要的关键字不存在
EKEYEXPIRED 127 关键字已过期
EKEYREVOKED 128 键值已取消
EKEYREJECTED 129 键值被服务所拒绝
EOWNERDEAD 130 拥有者已消逝
ENOTRECOVERABLE 131 状态无法回复
ERFKILL 132 由于 RF-kill 而无法操作
EHWPOISON 133 内存分页有硬件错误
ENOTSUP 95 不支持的操作
```



