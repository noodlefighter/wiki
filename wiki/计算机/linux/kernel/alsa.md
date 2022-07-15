> refers:
> 
> 原理
> 
> - [ALSA物理链路篇(上)](https://zhuanlan.zhihu.com/p/121614099)：这篇把各种ALSA内的各种机制讲清了

## alsa测试

> - [Linux: How to determine your audio card's, or USB mic's, maximum sampling rate - voxforge.org](http://www.voxforge.org/home/docs/faq/faq/linux-how-to-determine-your-audio-cards-or-usb-mics-maximum-sampling-rate)
> 
> - [ALSA --- amixer控制声卡驱动实现Line-in功能_jzzjsy的博客-CSDN博客](https://blog.csdn.net/jzzjsy/article/details/38872211)

测试播放：

```
$ aplay test.wav
```

测试录音：

```
$ arecord -f dat -r 48000 -D hw:0,0 -d 5 test.wav
```

切换音频采集的接口，scontrols命令获取可用枚举列表，sget读、sset写：

```
# ./amixer sget 'Left Capture Mux'
Simple mixer control 'Left Capture Mux',0
  Capabilities: enum
  Items: 'IN1L' 'IN2L' 'IN3L'
  Item0: 'IN2L'
# ./amixer sset 'Left Capture Mux' 'IN1L'
Simple mixer control 'Left Capture Mux',0
  Capabilities: enum
  Items: 'IN1L' 'IN2L' 'IN3L'
  Item0: 'IN1L'
```

## alsa路由routing

内部

> - 定义 SPKMIXL 相关路由：
> 
> ```c
> static const struct snd_soc_dapm_route intercon[] = {
>     // ...
>     { "SPKL", "DAC1 Switch", "DAC1L" },
>     { "SPKL", "DAC2 Switch", "DAC2L" },
> ```
> 
> 最终上层会看到两个控件：“SPKL DAC1 Switch”，“SPKL DAC2 Switch”；前者用于 “SPKL” 选中 “DAC1L” 作为输入，后者用于 “SPKL” 选中 “DAC2L” 作为输入。
> 
> 但控件 “SPKLDAC1 Switch” 或 “SPKL DAC2 Switch” 的打开，不代表能使得 “SPKL” 上电。只有当 “SPKL” 位于完整的音频路径中时，“SPKL” 才会上电。
> 
> via: ALSA物理链路篇(上)

可见，后一项作为前一项的输入，那么米尔的myb-6ulx板子的dts里wm8903的routing：

```
Headphone Jack      HPOUTL
Headphone Jack      HPOUTR
IN2L                Line In Jack
IN2R                Line In Jack
Mic                 MICBIAS
IN1L                Mic
```

即：`MICBIAS->Mic->IN1L`

结合`codec/wm8903.c`中的`wm8903_intercon`表：

```
static const struct snd_soc_dapm_route wm8903_intercon[] = {
    ...
    { "MICBIAS", NULL, "CLK_SYS" },
    ...
    { "Left Input Mux", "IN1L", "IN1L" },
    ...
    { "Left Input Inverting Mux", "IN1L", "IN1L" },
    ...
    { "Left Input Mode Mux", "Differential Line",
      "Left Input Mux" },
    ...
    { "Left Input Mode Mux", "Differential Mic",
      "Left Input Mux" },
};
```
