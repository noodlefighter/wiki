---

## GCC交叉编译

一般写Makefile时会把link时加的参数声明为`LDFLAGS`，所以当想设定库搜索路径时，可以写：

```
make LDFLAGS="-Wl,-rpath,/xxx/xx/libs"
```

```
-Wl,option
Pass option as an option to the linker. If option contains commas, it is split into multiple options at the commas. You can use this syntax to pass an argument to the option. For example, -Wl,-Map,output.map passes  -Map output.map to the linker. When using the GNU linker, you can also get the same effect with `-Wl,-Map=output.map'.

-rpath=dir

Add a directory to the runtime library search path. This is used when linking an ELF executable with shared objects. All -rpath arguments are concatenated and passed to the runtime linker, which uses them to locate shared objects at runtime. The -rpath option is also used when locating shared objects which are needed by shared objects explicitly included in the link;
```

设定sysroot

```
make LDFLAGS="--sysroot=/home/r/osp/buildroot-2019.02.1/output/host/arm-buildroot-linux-uclibcgnueabi/sysroot
```

## GCC生成MAP

```
gcc -o helloworld helloworld.c -Wl,-Map,helloworld.map
```

### 分析gcc的map文件

可以用[fpvgcc](https://github.com/ebs-universe/fpv-gcc)，直接`pip install fpvgcc`即可安装：

```
$ fpvgcc --secc xxx.map
```

也可以用自己改的[linker-map-summary](https://github.com/noodlefighter/linker-map-summary)

## undefined behavior [-Waggressive-loop-optimizations]

```
#define RGBLED_ROW  4
#define RGBLED_COL  4
static uint8_t _g_rgb_data[RGBLED_ROW][RGBLED_COL][3];
```
```
channel = 0;
for (i = 0; i < RGBLED_ROW; i++) {
    for (j = 0; j < RGBLED_COL; j++) {
        data[channel++] = (uint16_t) (_g_rgb_data[i][j][0] << 2);
        data[channel++] = (uint16_t) (_g_rgb_data[i][j][1] << 2);
        data[channel++] = (uint16_t) (_g_rgb_data[i][j][2] << 2);
    }
}
```

```
B:/Project/funckeyb/fw/funckeyb-fw/app/src/rgbled.c:174:33: warning: iteration 2 invokes undefined behavior [-Waggressive-loop-optimizations]
                 data[channel++] = (uint16_t) ((_g_rgb_data[i][j][0]) << 2);
                 ~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
B:/Project/funckeyb/fw/funckeyb-fw/app/src/rgbled.c:172:9: note: within this loop
         for (i = 0; i < RGBLED_ROW; i++) {
         ^~~

```

这里下标越界了 优化时出了问题 关掉优化就不会有这个警告
警告信息来看 是在loop-optimizations优化时 发现赋值操作行为未定义



## 警告：将一个整数转换为大小不同的指针 [-Wint-to-pointer-cast]

经常有需要把一个int通过void*传递，我们自己是知道int在32位内，32/64位机上的指针类型肯定能容纳这数据，但得把这意图告诉编译器，可以用intptr_t强转，它表示和指针长度相同的整数：

```
int转换成指针：
int   event;
void *to = (void*)(intptr_t)event;

指针转回int：
void *from;
int event = (int)(intptr_t)from;
```



## gcc+uclibc编译提示undefined reference to __fini_array_start

在使用buildroot配合自制的external工具链（gcc + uclibc）编译应用时提示`undefined reference to __fini_array_start`。

搜索了下发现是由于开启了动态链接，但找不到动态库`libc.so`，而退行链到了`libc.a`静态库导致的：

http://lists.buildroot.org/pipermail/buildroot/2011-June/043776.html

```none
Hi,

I've found that the target filesystem is missing /usr/lib/libc.so
(simple script) when choosing the native gcc compiler package.

This causes native gcc to fall back to static linking (libc.a), even
though "-shared" is specified. You can see this by observing gcc
-Wl,verbose output. When building shared code it returns this cryptic
error message:

/home/nn/buildroot/output/staging/usr/lib/libc.a(__uClibc_main.os): In
function `__uClibc_fini':
__uClibc_main.c:(.text+0x6c): undefined reference to `__fini_array_start'
__uClibc_main.c:(.text+0x74): undefined reference to `__fini_array_end'
/home/nn/buildroot/output/staging/usr/lib/libc.a(__uClibc_main.os): In
function `__uClibc_main':
__uClibc_main.c:(.text+0x250): undefined reference to
`__preinit_array_start'
__uClibc_main.c:(.text+0x254): undefined reference to `__preinit_array_end'
__uClibc_main.c:(.text+0x25c): undefined reference to `__init_array_start'
__uClibc_main.c:(.text+0x260): undefined reference to `__init_array_end'
/home/nn/buildroot/output/staging/usr/arm-linux-uclibcgnueabi/bin/ld:
./libgcc_s.so.1.tmp: hidden symbol `__fini_array_end' isn't defined
/home/nn/buildroot/output/staging/usr/arm-linux-uclibcgnueabi/bin/ld:
final link failed: Nonrepresentable section on output
collect2: ld returned 1 exit status
make[3]: *** [libgcc_s.so] Error 1

Here's a patch:

diff -ruN buildroot-2011.05/scripts/copy.sh
buildroot-2011.05-new/scripts/copy.sh
--- buildroot-2011.05/scripts/copy.sh    2011-05-27 16:18:21.000000000 +0200
+++ buildroot-2011.05-new/scripts/copy.sh    2011-06-30 16:02:59.059803037 +0200
@@ -6,6 +6,7 @@
 echo "Copying development files to target..."

 cp -af ${STAGING_DIR}/usr/include ${TARGET_DIR}/usr
+cp -af ${STAGING_DIR}/usr/lib/libc.so ${TARGET_DIR}/usr/lib/libc.so

 for LIBSDIR in /lib /usr/lib; do
     for WILDCARD in *.a *.la; do
```



## -fpermissive

-fno-permissive



## gcc 解决库交叉引用、顺序错误的问题

gcc是从右往左加载库的，比如存在静态库aaa和bbb，当bbb依赖aaa时，需要写成`-lbbb -laaa`，如果想临时解决这个问题（而不想大费周章地修改构建脚本），可以简单地用以下方式解决：

```
-Wl,--start-group -laaa -lbbb -Wl,--end-group
```

