

---



## 一般使用

```
mkdir build && cmake ..

多显示点信息，比如具体执行了什么命令
cmake -DCMAKE_VERBOSE_MAKEFILE=on .
```



## 交叉编译

> refers: 
>
> - https://gitlab.kitware.com/cmake/community/-/wikis/doc/cmake/CrossCompiling
> - https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html?highlight=cmake_c_compiler

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



自己最近用的：

```
# refers:
# - https://gitlab.kitware.com/cmake/community/-/wikis/doc/cmake/CrossCompiling
# - https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html?highlight=cmake_c_compiler

SET(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)

# rootfs
set(CMAKE_SYSROOT /opt/myir-imx-fb/4.1.15-2.0.1/sysroots/cortexa7hf-neon-poky-linux-gnueabi/)

# host-tools root
set(HOST_TOOLS_ROOT /opt/myir-imx-fb/4.1.15-2.0.1/sysroots/x86_64-pokysdk-linux)

# specify the cross compiler
SET(CMAKE_C_COMPILER   "${HOST_TOOLS_ROOT}/usr/bin/arm-poky-linux-gnueabi/arm-poky-linux-gnueabi-gcc")
SET(CMAKE_CXX_COMPILER "${HOST_TOOLS_ROOT}/usr/bin/arm-poky-linux-gnueabi/arm-poky-linux-gnueabi-g++")
set(CMAKE_C_FLAGS "-march=armv7ve -marm -mfpu=neon  -mfloat-abi=hard -mcpu=cortex-a7")
set(CMAKE_CXX_FLAGS "-march=armv7ve -marm -mfpu=neon  -mfloat-abi=hard -mcpu=cortex-a7")

# where is the target environment
SET(CMAKE_FIND_ROOT_PATH ${CMAKE_SYSROOT})

# for qmake, etc...
set(OE_QMAKE_PATH_EXTERNAL_HOST_BINS "${HOST_TOOLS_ROOT}/usr/bin/qt5/")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DQT_NO_OPENGL_ES_3")

# search for programs in the build host directories (not necessary)
SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)

# for libraries and headers in the target directories
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

# pkgconfig
set(ENV{PKG_CONFIG_DIR} "")
set(ENV{PKG_CONFIG_LIBDIR} "${CMAKE_SYSROOT}/usr/lib/pkgconfig:${CMAKE_SYSROOT}/usr/share/pkgconfig")
set(ENV{PKG_CONFIG_SYSROOT_DIR} ${CMAKE_SYSROOT})

```







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



## CMake目标别名



```
add_library(efence efence.c page.c print.c)
add_library(efence::efence ALIAS efence)
```





## CMake遇到过的问题



### 包含一个非子目录的CMake工程

比如：

```
add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/../../lib/CGame++
```

可能会报错：

```
CMake Error at CMakeLists.txt:6 (add_subdirectory):
add_subdirectory not given a binary directory but the given source
directory "/home/r/proj/asrx/asrx-main/lib/CGame++" is not a subdirectory
of "/home/r/proj/asrx/asrx-main/driver/drv_audio". When specifying an
out-of-tree source a binary directory must be explicitly specified.
```

必须指定目标目录，如此解决：

```
add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/../../lib/CGame++ ${CMAKE_BINARY_DIR}/CGame++)
```

