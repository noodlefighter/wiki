

---



## 一般使用

```
mkdir build && cmake ..
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