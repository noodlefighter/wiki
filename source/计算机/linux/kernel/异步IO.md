

---

使用fcntl()传入pid号注册异步, 驱动通过raise SIGIO/SIGURG信号实现异步通知.

* SIGIO: 一般IO
* SIGURG: 紧急IO



>  TODO: 整理	

<http://www.tutorialspoint.com/unix_system_calls/fcntl.htm>

<https://blog.csdn.net/wangkaiblog/article/details/17596367>