

目标，使用Linux的i2c-gpio，实现软件I2C，而且能在用户态下用它。

环境：板子是licheepi-nano，即suniv-f1c100s

工具：逻辑分析仪、i2cdetect



用户态i2c接口与Linux Kernel下文档`Documentation/i2c/dev-interface`有关，内核配置开启`CONFIG_I2C_CHARDEV`即可，不用做其他操作

用到了i2c-gpio.c这个驱动，对应binding文档`Documentation/devicetree/bindings/i2c/i2c-gpio.txt`，也开始对应内核配置`CONFIG_I2C_GPIO`，需要修改设备树，模仿文档，在dts中添加：

```
i2c {
        compatible = "i2c-gpio";
        sda-gpios = <&pio 4 12 GPIO_ACTIVE_HIGH>;
        scl-gpios = <&pio 4 11 GPIO_ACTIVE_HIGH>;
        i2c-gpio,delay-us = <2>;        /* ~100 kHz */
        #address-cells = <1>;
        #size-cells = <0>;
        status = "okay";
};
```

几条信息跟i2c-gpio有关：

```
[    0.114314] i2c-gpio soc:i2c0: error trying to get descriptor: -2
[    1.184205] gpio-139 (sda): enforced open drain please flag it properly in DT/ACPI DSDT/board file
[    1.193421] gpio-140 (scl): enforced open drain please flag it properly in DT/ACPI DSDT/board file
[    1.203392] i2c-gpio soc:i2c0: using lines 139 (SDA) and 140 (SCL)
```

第一条错误似乎可以忽略，参考[这个patch](https://code.ihub.org.cn/projects/825/repository/commit_diff?changeset=3747cd2efe7ecb9604972285ab3f60c96cb753a8)

这里在提示我需要把GPIO设置成开漏，所以继续修改dts：

```
i2c {
        compatible = "i2c-gpio";
        sda-gpios = <&pio 4 12 (GPIO_ACTIVE_HIGH|GPIO_OPEN_DRAIN)>;
        scl-gpios = <&pio 4 11 (GPIO_ACTIVE_HIGH|GPIO_OPEN_DRAIN)>;
        i2c-gpio,delay-us = <2>;        /* ~100 kHz */
        #address-cells = <1>;
        #size-cells = <0>;
        status = "okay";
};
```

与i2c-gpio相关的仅：

```
# i2cdetect 1
i2cdetect: WARNING! This program can confuse your I2C bus
Continue? [y/N] y
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- ^C
```

