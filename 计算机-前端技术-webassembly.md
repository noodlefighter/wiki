title: webassembly
date: 2019-11-12
categories:
- 计算机
- 前端技术




---

webassembly技术允许把本地代码在网页上执行，比如C/C++代码通过emscripten工具包就能方便地编译成网页上可执行的wasm格式。



## emscripten工具包

https://github.com/emscripten-core/emsdk

使用例：

```
$ ./emsdk install sdk-1.38.27-64bit
$ ./emsdk activate --embedded sdk-1.38.27-64bit
$ source emsdk_env.sh
```

这样就释放指定版本SDK到PATH环境变量中了。



### 文件系统

web通常不允许访问宿主本地文件系统。

emscripten提供了一个虚拟文件系统，打包时可以附加一些文件，这样就不用把文件内嵌在代码里了。



## emscripten工具包下编译QT

https://doc.qt.io/qt-5/wasm.html

版本一定要对，否则不一定编译得过。

使用编译出的qtbase/bin/qmake就可以用来编译



## webassembly技术与Immediate Mode GUI

界面上过多的DOM元素使浏览器渲染速度缓慢，使用立即式GUI是种解决方案，不创建对象保证快速渲染，例子：

https://pbrfrat.com/post/imgui_in_browser.html

https://github.com/jnmaloney/WebGui