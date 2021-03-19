---

> TODO 整理



电子书：Docker —— 从入门到实践

https://legacy.gitbook.com/book/yeasy/docker_practice/details

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
--env 设置环境变量, `--env XXXX=123`
-p    将容器的开放的端口映射到宿主上
--rm  程序退出时自动关闭容器
```

## 直接连接容器（操作命令行）

```
# docker run -itd xxx_image /bin/bash
（回一串sha）
# docker attach 这sha的前几位

直接操作运行中的容器：
# docker exec -it name-of-container bash
```



## 网络模式

* host模式，使用--net=host指定，网络不隔离直接用主机的网络

* container模式，使用--net=container:NAME_or_ID指定，与指定的容器共享同一网络
* none模式，使用--net=none指定，不使用网络

* bridge模式，使用--net=bridge指定，默认设置，默认无法访问宿主


## Docker Compose

部署docker的脚本工具，能方便地部署脚本，不用打很长的命令，也利于版本管理（不用自己写shell脚本了），如：

```
# file <docker-compose.yml>
version: "2"

networks:
  gitea:
    external: false

services:
  server:
    image: gitea/gitea:1.10.0
    environment:
      - USER_UID=1000
      - USER_GID=1000
    restart: always
    networks:
      - gitea
    volumes:
      - ./data:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "3000:3000"
      - "222:22"
```

命令：

```
部署(或者更新配置)
$ docker-compose up -d
撤销部署
$ docker-compose down
```



## 解决容器内创建的问题的权限问题



```
$ docker run --rm -it -u $UID:$GROUPS -v $PWD/platform:/opt/lichee jacklan/licheepi_nano /bin/bash
```



## 进入到docker容器中

```
$ docker exec -it containerID /bin/bash
```



## 镜象打包成tar、从tar还原

> 来源：https://jingsam.github.io/2017/08/26/docker-save-and-docker-export.html
>
> ## docker save和docker export的区别
>
> 总结一下docker save和docker export的区别：
>
> 1. docker save保存的是镜像（image），docker export保存的是容器（container）；
> 2. docker load用来载入镜像包，docker import用来载入容器包，但两者都会恢复为镜像；
> 3. docker load不能对载入的镜像重命名，而docker import可以为镜像指定新名称。



```
# docker save -o nginx.tar nginx:latest
# docker load -i nginx.tar
```



```
# docker export -o postgres-export.tar postgres
# docker import postgres-export.tar postgres:latest
```



## docker国内镜象、配置代理

冲国内使用docker、dockerhub仓库困难，需要配置镜象、代理。

编辑`/etc/docker/daemon.json`后：

```
{
  "registry-mirrors" : [
    "http://ovfftd6p.mirror.aliyuncs.com",
    "http://docker.mirrors.ustc.edu.cn"
  ],
  "insecure-registries" : [
    "docker.mirrors.ustc.edu.cn"
  ],
  "debug" : true,
  "experimental" : true
}
```

由于镜象可能不会同步dockerhub上的包，需要额外设置代理`/etc/systemd/system/docker.service.d/http-proxy.conf`：

```
[Service]
Environment="HTTP_PROXY=http://192.168.99.112:7890/" NO_PROXY=localhost,127.0.0.1,aliyuncs.com,tsinghua.edu.cn"
```

使生效：

```
$ sudo systemctl daemon-reload
$ systemctl show --property=Environment docker
$ sudo systemctl restart docker
```

## daocloud加速

https://www.daocloud.io/mirror

