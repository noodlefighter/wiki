title: 编译相关
date: 2019-06-12
categories:
- 计算机
- linux
- devtools


---

## 编译调试

打印更多信息

```
# 想看具体执行了什么命令
make V=1

# 想看makefile工作细节
make --debug=v
```

## 常见问题

### 没有规则可制作目标

* 文件名弄错了
* 搜索路径弄错了, 比如可以靠加搜索路径VPATH解决

### 没有指明目标并且找不到 makefile

可能是找不到include的makefile文件, 用 `make --debug=v`就能看到具体错误的地方.

## 交叉编译

设定库搜索路径
```
make LDFLAGS="-Wl,-rpath,/xxx/xx/libs"
```

```
-Wl,option
Pass option as an option to the linker. If option contains commas, it is split into multiple options at the commas. You can use this syntax to pass an argument to the option. For example, -Wl,-Map,output.map passes  -Map output.map to the linker. When using the GNU linker, you can also get the same effect with `-Wl,-Map=output.map'.

-rpath=dir

Add a directory to the runtime library search path. This is used when linking an ELF executable with shared objects. All -rpath arguments are concatenated and passed to the runtime linker, which uses them to locate shared objects at runtime. The -rpath option is also used when locating shared objects which are needed by shared objects explicitly included in the link;
```

设定sysroot
```
make LDFLAGS="--sysroot=/home/r/osp/buildroot-2019.02.1/output/host/arm-buildroot-linux-uclibcgnueabi/sysroot
```