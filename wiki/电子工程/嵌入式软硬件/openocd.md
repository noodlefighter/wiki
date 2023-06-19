

## openocd烧录程序

以CH32V208为例

```
./openocd -f ./wch-riscv.cfg -c init -c halt -c "flash erase_sector wch_riscv 0 last" -c "program /home/r/proj/nypx07/nypx-07-fw/build/fw/nypx07-fw.elf" -c "verify_image $1" -c wlink_reset_resume -c exit
```





## openocd开启关闭写保护

以CH32V208为例

```
./openocd -f wch-riscv.cfg -c init -c halt -c "flash protect wch_riscv 0 last  on " -c exit  开启读保护
./openocd -f wch-riscv.cfg -c init -c halt -c "flash protect wch_riscv 0 last  off " -c exit  关闭读保护
```

