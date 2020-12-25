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



## -fpermissive

-fno-permissive