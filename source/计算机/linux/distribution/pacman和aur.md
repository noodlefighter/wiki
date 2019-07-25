

---

## pacman是arch系下的包管理工具



```
# 更新所有包
pacman -Syu

# 搜索包
pacman -Ss xxx

# 安装包
pacman -S xxx

# 删除软件包，顺便移除没被其他包依赖的依赖包
pacman -Rs xxx
```

## AUR是非官方提供的包

为了安全，一般不是直接发布二进制包，而是一些包含编译脚本的信息。

使用`yay`可以方便地使用AUR：

```
pacman -S yay
```

yay支持pacman风格的命令，挪过来就能用。

