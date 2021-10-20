

## ARM 进入 HardFault 的处理方法

![微信图片_20210901180305](_assets/arm/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20210901180305.png)

用 Jlink Commander 连上，观察xPSR的值，最低的数字为中断号：

![xpsr](_assets/arm/xpsr.jpg)

### 手动DUMP出调用栈

看MSP的值，dump出栈上内容：

![微信图片_20210901180858](_assets/arm/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20210901180858.png)

### DUMP 出 Flash 内容

![微信图片_20210901181015](_assets/arm/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20210901181015.jpg)

