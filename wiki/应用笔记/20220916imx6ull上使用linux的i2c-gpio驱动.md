
> IMX6ULL
> Linux 4.1.15

使用IMX6ULL时发现，一旦硬件I2C受到干扰，I2C驱动就会陷入卡死的状态，表现为ioctl操作一直返回22（-EAGAIN，resource temporarily unavailable），无法恢复，比如我现在调试的板子使用了FM接收芯片，一旦FM发射源离得很近，I2C总线就会死掉

虽然干扰的路径未知，但总不希望软件这么脆弱，所以尝试开启GPIO实现的I2C总线，大致思路：

- 开启GPIO实现的I2C驱动`CONFIG_I2C_GPIO=y`，并配置设备树
- 设备树中配置pinmux，配置对应的IO复用功能为GPIO
- 用户态i2c接口与Linux Kernel下文档`Documentation/i2c/dev-interface`有关，内核配置开启`CONFIG_I2C_CHARDEV`




i2c-gpio.c驱动，对应binding文档`Documentation/devicetree/bindings/i2c/i2c-gpio.txt`：

```
Device-Tree bindings for i2c gpio driver

Required properties:
	- compatible = "i2c-gpio";
	- gpios: sda and scl gpio


Optional properties:
	- i2c-gpio,sda-open-drain: sda as open drain
	- i2c-gpio,scl-open-drain: scl as open drain
	- i2c-gpio,scl-output-only: scl as output only
	- i2c-gpio,delay-us: delay between GPIO operations (may depend on each platform)
	- i2c-gpio,timeout-ms: timeout to get data

Example nodes:

i2c@0 {
	compatible = "i2c-gpio";
	gpios = <&pioA 23 0 /* sda */
		 &pioA 24 0 /* scl */
		>;
	i2c-gpio,sda-open-drain;
	i2c-gpio,scl-open-drain;
	i2c-gpio,delay-us = <2>;	/* ~100 kHz */
	#address-cells = <1>;
	#size-cells = <0>;

	rv3029c2@56 {
		compatible = "rv3029c2";
		reg = <0x56>;
	};
};

```



开启内核配置`CONFIG_I2C_GPIO=y`，模仿文档修改设备树，dts中添加：

```
	i2c1_gpio {
		#address-cells = <1>;
		#size-cells = <0>;
		compatible = "i2c-gpio";
		gpios = <
			&gpio1 29 GPIO_ACTIVE_HIGH /* SDA */
			&gpio1 28 GPIO_ACTIVE_HIGH /* SCL */
		>;
		i2c-gpio,delay-us = <5>;	/* ~100 kHz */
		status = "okay";
	};
```

添加IO复用配置：

```
		pinctrl_hog_1: hoggrp-1 {
			fsl,pins = <
				...
				
				/*
					模块pin64, GPIO1_28, I2C1_SCL
					模块pin65, GPIO1_29, I2C1_SDA
				*/
				MX6UL_PAD_UART4_TX_DATA__GPIO1_IO28 0x1b0b1
				MX6UL_PAD_UART4_RX_DATA__GPIO1_IO29 0x1b0b1
			>;
		};
```

重新烧上内核和DTB：

```
root@ebsx-imx6ull:~# dmesg |grep i2c
i2c-gpio i2c1: using pins 29 (SDA) and 28 (SCL)
root@ebsx-imx6ull:~# ls /dev | grep i2c
i2c-1
i2c-3
i2c-4
root@ebsx-imx6ull:~# i2cdetect -l
i2c-1	i2c       	21a4000.i2c                     	I2C adapter
i2c-3	i2c       	21f8000.i2c                     	I2C adapter
i2c-4	i2c       	i2c1                            	I2C adapter
root@ebsx-imx6ull:~# i2cdetect -y 4
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: 10 11 -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: 60 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

一切正常，打完收工！

