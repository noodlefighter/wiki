

# multipass - 跨平台ubuntu虚拟机环境

一个命令行下方便使用的ubuntu虚拟机环境, 临时搭个环境挺方便

https://multipass.run/docs

```
$ snap install multipass

$ multipass launch ubuntu --name ubuntu --disk 50G --cpus 8
$ multipass mount . ubuntu:/home/r/lede
$ multipass shell ubuntu
```



