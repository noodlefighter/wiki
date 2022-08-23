

## pyocd+vscode调试mcu

原料：

- vscode
- vscode cortex-debug插件
- pyocd

参考：

- [pyOCD文档](https://github.com/pyocd/pyOCD/blob/master/docs/target_support.md)
  - [关于支持 的taget的说明](https://github.com/pyocd/pyOCD/blob/master/docs/target_support.md)
  - [gdb命令参考](https://github.com/pyocd/pyOCD/blob/master/docs/command_reference.md)：用这些命令前加`monitor`，比如`break`命令，要在gdb里输入`monitor break`
- [cortex-debug的Wiki](https://github.com/Marus/cortex-debug/wiki)
  - [关于pyOCD的说明](https://github.com/Marus/cortex-debug/wiki/PyOCD-Specific-Configuration-Options)

配置：

1. 先找到目标的名字，比如`stm32f412xe`，填入launch配置：

```
$ pyocd list --target
```

> 这和flash烧录算法有关，如果没有对应的target请参考pyOCD文档，下载对应的pack

2. vscode的`launch.json`:

```
{
    "version": "0.2.0",
    "configurations": [
      {
        "name": "Release",
        "cwd": "${workspaceRoot}",
        "executable": "./build/rrr.elf",
        "request": "launch",
        "type": "cortex-debug",
        "servertype": "pyocd",
        "interface": "swd",
        "targetId": "stm32f412xe",
        "runToMain": true,
        "preLaunchCommands": [
          "load",
        ],
        "preRestartCommands": [
          "monitor reset"
        ]
      }
    ]
  }
```





## 为PyOCD添加新MCU Target

1)下载pyocd源码

git clone https://github.com/pyocd/pyOCD.git 
注意要把python升级到3.9以上，这个倒霉孩子python3.8就不正常了

主要是为了 使用 scripts/generate_flash_algo.py  ，用来从 elf 抽取 算法文件。

2）执行 generate_flash_algo.py le5010.elf (FLM) ，如果正常它会生成一个 pyocd_blob.py

但是大概率会直接崩溃，在这里

/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/pyocd/target/pack/flash_algo.py

可以找我，我教你怎么修复这个BUG。

3)查找pyocd安装路径
                      pip show pyocd

5)添加target

在目录/usr/local/lib/python3.9/site-packages/pyocd/target/builtin/

随便复制一个出来修改。

把生成出来的 pyocd_blob.py copy 进去即可

