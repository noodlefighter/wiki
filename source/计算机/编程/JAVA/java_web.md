
---


http://wiki.jikexueyuan.com/project/spring/ioc-containers.html
https://www.cnblogs.com/hisen/p/6800365.html

https://spring.io/guides/gs/rest-service/
https://spring.io/understanding/REST

博客实现
https://blog.csdn.net/xp541130126/article/details/70665917

 SwaggerUI API接口文档
 
 IoC控制反转，IoC容器=控制反转容器
 
 数据访问对象 (DAO) 模式

学习笔记，边学边写。

## 初探Web

在这之前，对于当前的Web技术认识都来源于和程序员朋友的日常聊天，什么前后端分离，MVC，MVVM，Control，面向切片编程，都是道听途说云里雾里。

很久以前，站长们只需要一个能存放动态网页的虚拟主机和sql数据库服务器就能满足需要，把网页（html, asp, php文件）放进主机空间，少许配置就能跑起。

但现在做网站，很多时候需要用到VPS，因为有些网站程序已经不只是动态网页脚本，比如使用了一些框架Node.JS、flask（python）、ROR（ruby）需要在服务器上运行程序。

趁现在在家里蹲着，试着扩展一下技能树，从主流的Java Web入手学习，顺便做个just for fun的小项目：

* 云表情包的后端系统
* 多用户
* 用户可以上传表情，上传相同表情时自动选取合适的高考

## Java Web 

似乎主流就俩组合：
SSH = Struts+Spring+Hibernate
SSM = Spring+SpringMVC+MyBatis   

据说SSM略新，就从它下手吧，逐个先看看是个什么东西。

### Spring

[主页](https://spring.io/)逛逛。

```
End-to-end support for reactive & servlet based apps on the JVM. 
```

根据描述`reactive`响应式的架构是5.0支持的新东西，并发性能强，先不理会。

重点在`servlet`上，“JVM上基于servlet的应用”是个什么东西呢？查[wiki](https://zh.wikipedia.org/wiki/Java_Servlet)可知servlet就是实现了servlet的类，用于服务器程序收到客户端请求时执行做些处理后返回数据，wiki里描述它的工作模式：

```
工作模式
1. 客户端发送请求至服务器
2. 服务器启动并调用Servlet，Servlet根据客户端请求生成响应内容并将其传给服务器
3. 服务器将响应返回客户端
```

### SpringMVC

MVC就是模型Model、视图View、控制器Controller，分离了业务数据、界面显示和业务逻辑。

当


模型负责

### MyBatis

[官方文档](http://www.mybatis.org/mybatis-3/zh/index.html)

一款持久层框架，能避免手写JDBC代码，使用简单的XML和注解类配置和映射原生信息，将接口和Java对象映射成数据库中的记录。

### 查资料的过程中遇到的相关东西

熟悉的面孔`Apache Tomcat`，一个Web服务器，这里有[IBM的一篇文章](https://www.ibm.com/developerworks/cn/java/j-lo-servlet/)介绍了Tomcat和Servlet体系，功能：
* 跑JSP，能把JSP转换成对应Servlet
* 提供Servlet引擎

`maven`，用于管理依赖，目前理解为java世界的包管理器。

`druid`，阿里的数据源，连接池。

`Spring Boot`能帮助快速建立
