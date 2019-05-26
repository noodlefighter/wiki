
---

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
