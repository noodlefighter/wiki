

---



## 一般使用

```
mkdir build && cmake ..

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

一个有价值的参考是openembedded的cmake.bbclass通用交叉编译过程：https://github.com/openembedded/openembedded/blob/master/classes/cmake.bbclass



## CMake寻找依赖库

> refers:
>
> - 文档 [target_link_directories](https://cmake.org/cmake/help/latest/command/target_link_directories.html?highlight=link_directories#command:target_link_directories)
> - https://stackoverflow.com/questions/29191855/what-is-the-proper-way-to-use-pkg-config-from-cmake

一个用PkgConfig模块的例子，这里对应OS为Linux的场合，其他OS应该分别处理：

```
find_package(PkgConfig REQUIRED)
pkg_check_modules(AVCODEC REQUIRED libavcodec)
pkg_check_modules(SWSCALE REQUIRED libswscale)
pkg_check_modules(AVUTIL REQUIRED libavutil)
pkg_check_modules(AVFORMAT REQUIRED libavformat)
pkg_check_modules(SWRESAMPLE REQUIRED libswresample)
pkg_check_modules(AVFILTER REQUIRED libavfilter)
set(FFMPEG_LIBS ${AVCODEC_LIBRARIES} ${SWSCALE_LIBRARIES} ${AVUTIL_LIBRARIES} ${AVFORMAT_LIBRARIES} ${SWRESAMPLE_LIBRARIES} ${AVFILTER_LIBRARIES})
set(FFMPEG_INCS ${AVCODEC_INCLUDE_DIRS} ${SWSCALE_INCLUDE_DIRS} ${AVUTIL_INCLUDE_DIRS} ${AVFORMAT_INCLUDE_DIRS} ${SWRESAMPLE_INCLUDE_DIRS} ${AVFILTER_INCLUDE_DIRS})
set(FFMPEG_LIBDIRS ${AVCODEC_LIBRARY_DIRS} ${SWSCALE_LIBRARY_DIRS} ${AVUTIL_LIBRARY_DIRS} ${AVFORMAT_LIBRARY_DIRS} ${SWRESAMPLE_LIBRARY_DIRS} ${AVFILTER_LIBRARY_DIRS})

add_library(ebsx ${EBSX_SRC})
target_link_libraries(ebsx ${FFMPEG_LIBS})
target_include_directories(ebsx PUBLIC ${FFMPEG_INCS})
target_link_directories(ebsx PUBLIC ${FFMPEG_LIBDIRS})
```



## CMake中描述安装

> refers:
>
> - https://cmake.org/cmake/help/latest/command/install.html

安装一个目标：

```
install(TARGETS <目标名...>)
```

