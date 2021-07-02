

## 命令行下编译 MDK 工程

国产 MCU 只提供了 MDK 开发环境，由于平时用 Linux 桌面，而且不想折腾环境，所以直接通过 SSH，远程到 Windows 上开发。

参考：https://www.keil.com/support/man/docs/uv4/uv4_commandline.htm

```
$ cat build.sh
touch log.txt
tail -f log.txt &
/c/Keil_v5/UV4/UV4.exe -j0 -b sig_mesh_provee.uvprojx -o log.txt
```

`-j0`不显示 GUI，`tail -f` 实时监看输出的log