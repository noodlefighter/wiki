

# 荔枝派Nano（Lichee Pi Nano）相关

## 启动流程


1. BOOT ROM会根据TF卡、SPI FLASH的顺序尝试引导，若失败，则进入FEL模式，此时可以用sunxi-tool操作
2. 进入uboot
3. uboot引导linux


##  references

[荔枝派nano(f1c100s)的SPI-Flash系统编译创建全过程](https://whycan.cn/t_2179.html)





## 备用



SPI驱动选项：CONFIG_SUN6I_SPI