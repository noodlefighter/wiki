

---



## 一般使用

```
mkdir build && cmake ..
```

## 调试

```
多显示点信息，比如具体执行了什么命令
cmake -DCMAKE_VERBOSE_MAKEFILE=on .
```



## 交叉编译



Makefile:

```
all: local

local:
	cmake --debug -S. -B_build -G "Unix Makefiles"
	cd _build && make

win32:
	cmake -S. -B_build_win32 -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE=./mingw-w64-i686.cmake
	cd _build_win32 && make

win64:
	cmake -S. -B_build_win64 -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE=./mingw-w64-x86_64.cmake
	cd _build_win64 && make
```



可以参考OpenWRT的构建脚本`cmake.mk`：https://github.com/openwrt/openwrt/blob/master/include/cmake.mk

比如之前编译box86这个项目：

```
rm -rf build/
mkdir build
cd build/

CROSS=arm-linux-gnueabihf-
CC=${CROSS}gcc

CFLAGS="-march=armv8-a -mtune=cortex-a53" \
cmake .. \
        -DARM_DYNAREC=ON \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DCMAKE_SYSTEM_PROCESSOR=arm \
        -DCMAKE_C_COMPILER=${CC}

make -j8
```

