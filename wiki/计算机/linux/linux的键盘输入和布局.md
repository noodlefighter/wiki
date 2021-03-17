

---

linux的输入子系统，`/dev/input/*`，查看设备列表：

```
￥ cat /proc/bus/input/devices
```

## 通过设备文件读input event

`/dev/input/evnet*`，可以读、阻塞读、select。

`#include <linux/input.h>`：

```
struct input_event {
      struct timeval time;
      unsigned short type;
      unsigned short code;
      unsigned int value; 
};
```

## 触摸屏库tslib

https://github.com/libts/tslib

电阻式触摸屏的输入需要校准、与显示屏尺寸对应，tslib就能实现这些需求。

Debian的源里叫`libts`，README.md，参考`man ts.conf`。

触摸屏校准（校准信息被存放在`/etc/pointercal`里）：

```
$ sudo TSLIB_TSDEVICE=/dev/input/event0 TSLIB_FBDEVICE=/dev/fb1 ts_calibrate
```

校准后测试：

```
$ sudo TSLIB_TSDEVICE=/dev/input/event0 TSLIB_FBDEVICE=/dev/fb1 ts_test
```

开启input event服务：

```
$ sudo TSLIB_TSDEVICE=/dev/input/event0 ts_uinput -d
```

服务开启后，查看设备：

```
$ cat /proc/bus/input/devices

...(略)

I: Bus=0006 Vendor=0000 Product=0000 Version=0000
N: Name="ts_uinput"
P: Phys=
S: Sysfs=/devices/virtual/input/input2
U: Uniq=
H: Handlers=mouse1 event1
B: PROP=0
B: EV=b
B: KEY=400 0 0 0 0 0 0 0 0 0 0
B: ABS=1000003
```

库的`README.md`中提到“symlink /dev/input/ts_uinput to to the new event file”的两种方式：用脚本链接（传统方式）、写udev的rules。

写udev的rules的方式比较优秀，还能顺便把tslib要用的event设备映射成`/dev/input/ts`，`/etc/udev/rules.d/98-touchscreen.rules`：

```
SUBSYSTEM=="input", KERNEL=="event[0-9]*", ATTRS{name}=="NAME_OF_THE_TOUCH_CONTROLLER", SYMLINK+="input/ts", TAG+="systemd" ENV{SYSTEMD_WANTS}="ts_uinput.service"
SUBSYSTEM=="input", KERNEL=="event[0-9]*", ATTRS{name}=="ts_uinput", SYMLINK+="input/ts_uinput"
```

## 测试工具evtest

截图是测试一个触摸屏`/dev/input/event0`

![1569472849646](_assets/linux的input子系统/1569472849646.png)

## Linux下的键盘布局

archlinuxu的wiki上的说明：

https://wiki.archlinux.org/index.php/Linux_console/Keyboard_configuration

loadkeys:

https://jlk.fjfi.cvut.cz/arch/manpages/man/loadkeys.1

问答：

https://superuser.com/questions/729585/remap-keys-without-xmodmap-or-any-x-tools#comment1565295_729585

https://stackoverflow.com/questions/34582279/linux-c-keymapping-keycodes


在linux中，输入设备在input子系统中被抽象，如`/dev/input/event*`，我们能拿到的keycode在这里被归一。测试按键，获得keycode：

```
# showkeys -a
```

只有keycode是不足以在console上输入字符的，因为不同的键盘布局上的同一个键打出来的字符是不一样的，比如Shift+2在US布局里是“@”而欧洲布局里是欧元符号，所以linux还有一套从keycode转换到字符的机制。

从linux的map文件生成c语言数组的map表：

```
# loadkeys --mktable defkeymap.map
```

查看当前映射表：

```
# dumpkeys
```