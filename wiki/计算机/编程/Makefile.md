---

## 编译调试

打印更多信息

```
# 想看makefile工作细节
make --debug=v
```

## 常见问题

### 没有规则可制作目标

* 文件名弄错了
* 搜索路径弄错了, 比如可以靠加搜索路径VPATH解决

### 没有指明目标并且找不到 makefile

可能是找不到include的makefile文件, 用 `make --debug=v`就能看到具体错误的地方.



## Makefile包含目录下所有源文件

```
USR_SRCS += $(wildcard $(SRCDIR)/*.c)
```

