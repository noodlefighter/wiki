

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

