---

> TODO 整理



概念
https://www.cnblogs.com/vikings-blog/p/3958091.html


https://hub.docker.com/r/resin/rpi-raspbian/

nignx/php image build:
http://blog.topspeedsnail.com/archives/8084

搭嵌入式开发环境
https://blog.csdn.net/zhanglianpin/article/details/80256028

在x86平台上构建arm容器
https://www.balena.io/blog/building-arm-containers-on-any-x86-machine-even-dockerhub/

http://tinylab.org/docker-qemu-linux-lab/

镜象/容器导出导入
https://blog.csdn.net/liukuan73/article/details/78089138

helloworld
https://www.cnblogs.com/herui1991/p/7468583.html

Docker镜像的创建、存出、载入
https://www.cnblogs.com/zhangmingcheng/p/5720792.html

在任何x86机器上构建ARM容器，甚至是DockerHub
https://www.balena.io/blog/building-arm-containers-on-any-x86-machine-even-dockerhub/

docker入门——构建镜像
https://www.cnblogs.com/Bourbon-tian/p/6867796.html

树莓派docker
http://dockone.io/article/1732

快速入门文章
https://blog.csdn.net/jian1jian_/article/details/66475698?locationNum=7&fps=1

如何创建docker镜象
https://blog.csdn.net/kity9420/article/details/75717091



## 运行容器

```
# docker run -it <镜象名> <要执行的程序>
```

常用选项

```
-d    demon常驻
-v    映射宿主目录到容器（应该和mount --bind相同）
```

## 直接连接容器（操作命令行）

```
# docker run -itd xxx_image /bin/bash
（回一串sha）
# docker attach 这sha的前几位
```

