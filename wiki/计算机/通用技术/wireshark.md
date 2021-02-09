---

## wireshark二次开发

captrue options - interface management, pipes, 选择文件

怎么通过管道把数据给到wireshark，这个wiki说得很详细了：
https://wiki.wireshark.org/CaptureSetup/Pipes

官方lua说明和参考
https://www.wireshark.org/docs/wsdg_html_chunked/wsluarm.html
https://www.wireshark.org/docs/wsdg_html_chunked/wsluarm_modules.html

lua插件例子
https://yoursunny.com/t/2008/Wireshark-Lua-dissector/
https://www.zybuluo.com/natsumi/note/77991
（这篇讲得最全）https://www.cnblogs.com/ascii0x03/p/8781643.html

tcp粘包
https://blog.csdn.net/huolangwangyi/article/details/51010152

命令行加载lua脚本
```
The command line option -X lua_script:file.lua can be used to load Lua scripts as well.
```

一个叫ZeroBrane Studio的IDE提供的lua调试方法
http://notebook.kulchenko.com/zerobrane/debugging-wireshark-lua-scripts-with-zerobrane-studio

lua学习
https://blog.csdn.net/cxihu/article/details/78769594
https://www.runoob.com/lua/lua-object-oriented.html

lua坑
http://www.blogjava.net/rockblue1988/archive/2014/12/29/421910.html



## wireshark usb抓包

### Linux

```
$ modprobe usbmon
$ sudo wireshark
```

usbmon<X>就是usb根设备

