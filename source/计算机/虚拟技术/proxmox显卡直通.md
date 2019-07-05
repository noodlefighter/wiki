

---

打算利用虚拟化平台做双系统桌面环境，作娱乐、开发一体的主机。

折腾了几天proxmox显卡直通，linux那按照官方的wiki里的方法直接能用，但win安装显卡驱动始终是（code: 43）。

直接dump bios rom的方法一直没成功，rom-paser发现是坏的。直到看到了下面的参考文章，提出了其他的dump方式。

我的机器情况：

```
Intel E3-1230v2
Nvidia GTX750
```

参考：

https://forums.unraid.net/topic/41951-gpu-passthrough-with-only-one-card/

## 参考文章

> title: 终于搞定了KVM下的GPU Passthrough
> via: <http://m.newsmth.net/article/DigiHome/684698>

配置参考这个文档
https://pve.proxmox.com/wiki/Pci_passthrough    ...(1)
但弄完之后在Windows里就Code: 43

这个回答解决了一个重大问题
http://stackoverflow.com/questions/41362981/nvidia-gpu-passthrough-fail-with-code-43                                            ...(2)

把配置要点描述如下：

0. 用UEFI装系统
1. 完整按照(1)的描述做一遍
2. 带声卡的显卡，比如显卡是01:00.0，声卡是01:00.1，直接写01:00.0，真要声卡的话再写一行hostpci，不要合写成01:00
3. 在grub里加上这句：video=efifb:off（不太确定相关性）
4. 按照(2)的说法，你需要自己指定romfile，但是它给的dump方法（两文写的方法一样）并不能用！(2)说你需要临时用另一个显卡启动，但我没有另一个显卡。。。

成功地dump显卡rom方案是：https://github.com/envytools/envytools
下载并编译这个工具，里面有一个nvagetbios，直接执行会说invalid signature之类的，要加-s参数：

```
nvagetbios -s prom > vbios.bin
```
这个方法在我这是好使的，得到的vbios.bin可以用rom_parser验证一下：

```
Valid ROM signature found @0h, PCIR offset 1a0h
        PCIR: type 0 (x86 PC-AT), vendor: 10de, device: 1c81, class: 030000
        PCIR: revision 0, vendor revision: 1
Valid ROM signature found @f000h, PCIR offset 1ch
        PCIR: type 3 (EFI), vendor: 10de, device: 1c81, class: 030000
        PCIR: revision 3, vendor revision: 0
                EFI: Signature Valid, Subsystem: Boot, Machine: X64
        Last image
```

如果显示Error, ran off the end之类的就是出错了

最终写在配置文件的那句话是这样的：

```
hostpci0: 01:00.0,pcie=1,x-vga=on,romfile=vbios.bin
```

然后启动系统，如果没啥问题的话Proxmox的虚拟机启动画面就会显示在真实显示器上
（注意这样配置了之后VNC和网页控制台就不能用了），装了Windows之后就像正常机器一样，Nvidia的驱动也可以随便装。



## Nvidia GPU passthrough fail with code 43

> via: <https://stackoverflow.com/questions/41362981/nvidia-gpu-passthrough-fail-with-code-43>

You need to pass copy of unmodified videocard ROM to VM.

- You need a secondary GPU that you can use as the primary for this
  process. **You cannot dump a clean copy of the BIOS without having the passthrough GPU as a secondary card**

- Put the extra card in the primary slot and the intended passthrough card in another pci-e port and bootup.

- Find your intended GPU again via lspci -v. In my case it had about the same address.

- Now you can dump the ROM to a file:

  ```
  # echo "0000:05:00.0" > /sys/bus/pci/drivers/vfio-pci/unbind
  # cd /sys/bus/pci/devices/0000\:05\:00.0
  # echo 1 > rom 
  # cat rom > /home/username/KVM/evga_gtx970.dump
  # echo 0 > rom
  # echo "0000:05:00.0" > /sys/bus/pci/drivers/vfio-pci/bind
  ```

  In this case, 0000:05:00.0 is my PCI card address. You don't really need the bind step at the bottom since you'll be rebooting anyways.

- You can check the integrity of the ROM dump with this handy utility at <https://github.com/awilliam/rom-parser>. My rom looks like:

  ```
  # ./rom-parser evga_gtx970.dump
  Valid ROM signature found @0h, PCIR offset 1a0h
          PCIR: type 0 (x86 PC-AT), vendor: 10de, device: 13c2, class: 030000
          PCIR: revision 0, vendor revision: 1
  Valid ROM signature found @f400h, PCIR offset 1ch
          PCIR: type 3 (EFI), vendor: 10de, device: 13c2, class: 030000
          PCIR: revision 3, vendor revision: 0
                  EFI: Signature Valid, Subsystem: Boot, Machine: X64
  Last image
  ```

  You should have both an EFI and a non-EFI x86 ROM in the dump ( I think most cards have both)

- Turn off the machine and put your GTX 1070 back in the primary slot.

- After booting, edit your VM xml and in the section for your GPU (if you have already assigned the GPU to the VM) there should be a section. Add a file='path/to/dump/here' statement to it. My full section looks like:

```
  <hostdev mode='subsystem' type='pci' managed='yes'>
    <source>
      <address domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
    </source>
    <rom bar='on' file='/home/username/KVM/evga_gtx970.dump'/>
    <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
  </hostdev>
```

  This will have the VM start the card with that BIOS instead of whatever the kernel gives it.

[source](https://www.reddit.com/r/VFIO/comments/5sh41p/any_other_reasons_for_nvidia_driver_code_43/)

**Please note that you have to use OVMF (EFI) because SeaBIOS does not use card ROM properly.**

## proxmox显卡直通后 无法用ISO启动 提示DVDROM boot timeout

弄好直通指定pcie设备的romfile后，屏幕上出现proxmox的BIOS界面，却无法光盘引导了，明明找到了设备，却提示timeout：

