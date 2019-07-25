

---

linux上有epoll做高并发，看到了这篇关于异步事件驱动库的文章：https://blog.csdn.net/lijinqi1987/article/details/71214974

发现libev在windows上的实现用的是一种叫IOCP的接口，应该能同linux的epoll类比。



