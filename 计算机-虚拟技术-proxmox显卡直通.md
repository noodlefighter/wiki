title: proxmox显卡直通
date: 2019-07-08
categories:
- 计算机
- 虚拟技术




---

打算利用虚拟化平台做双系统桌面环境，作娱乐、开发一体的主机。

折腾了几天proxmox显卡直通，linux那按照官方的wiki里的方法直接能用，但win安装显卡驱动始终是（code: 43）。

直接dump bios rom的方法一直没成功，rom-paser发现是坏的。直到看到了下面的参考文章，提出了其他的dump方式。

我的机器情况：

```
Intel E3-1230v2
Nvidia GTX750
```

成功的配置
```
/usr/bin/kvm -id 101 -name r-win-home -chardev socket,id=qmp,path=/var/run/qemu-server/101.qmp,server,nowait -mon chardev=qmp,mode=control -ch
ardev socket,id=qmp-event,path=/var/run/qmeventd.sock,reconnect=5 -mon chardev=qmp-event,mode=control -pidfile /var/run/qemu-server/101.pid -daemonize -smbios type=1,uuid=99242359-1d91-4bc7-aa21-22c43f343590
 -drive if=pflash,unit=0,format=raw,readonly,file=/usr/share/pve-edk2-firmware//OVMF_CODE.fd -drive if=pflash,unit=1,format=raw,id=drive-efidisk0,file=/tmp/101-ovmf.fd -smp 8,sockets=1,cores=8,maxcpus=8 -nodefaults -boot menu=on,strict=on,reboot-timeout=1000,splash=/usr/share/qemu-server/bootsplash.jpg -vnc unix:/var/run/qemu-server/101.vnc,x509,password -no-hpet -cpu kvm64,+lahf_lm,+sep,+kvm_pv_unhalt,+kvm_pv_eoi,hv_vendor_id=proxmox,hv_spinlocks=0x1fff,hv_vapic,hv_time,hv_reset,hv_vpindex,hv_runtime,hv_relaxed,hv_synic,hv_stimer,enforce,kvm=off -m 8192 -device vmgenid,guid=94140d79-7ee3-414f-9e09-7394e7785f97 -readconfig /usr/share/qemu-server/pve-q35.cfg -device nec-usb-xhci,id=xhci,bus=pci.1,addr=0x1b -device vfio-pci,host=01:00.0,id=hostpci0,bus=ich9-pcie-port-1,addr=0x0,romfile=/usr/share/kvm/gtx750.rom -device vfio-pci,host=00:1a.0,id=hostpci1,bus=ich9-pcie-port-2,addr=0x0 -device usb-host,bus=xhci.0,hostbus=4,hostport=1,id=usb2 -chardev spicevmc,id=usbredirchardev3,name=usbredir -device usb-redir,chardev=usbredirchardev3,id=usbredirdev3,bus=ehci.0 -device qxl-vga,id=vga,bus=pcie.0,addr=0x1 -spice tls-port=61000,addr=127.0.0.1,tls-ciphers=HIGH,seamless-migration=on -device virtio-serial,id=spice,bus=pci.0,addr=0x9 -chardev spicevmc,id=vdagent,name=vdagent -device virtserialport,chardev=vdagent,name=com.redhat.spice.0 -device virtio-balloon-pci,id=balloon0,bus=pci.0,addr=0x3 -iscsi initiator-name=iqn.1993-08.org.debian:01:373ed23ccfe4 -drive file=/var/lib/vz/template/iso/virtio-win-0.1.171.iso,if=none,id=drive-ide2,media=cdrom,aio=threads -device ide-cd,bus=ide.1,unit=0,drive=drive-ide2,id=ide2,bootindex=200 -drive file=/dev/ssd/vm-101-disk-0,if=none,id=drive-virtio0,format=raw,cache=none,aio=native,detect-zeroes=on -device virtio-blk-pci,drive=drive-virtio0,id=virtio0,bus=pci.0,addr=0xa,bootindex=100 -drive file=/dev/sda,if=none,id=drive-virtio1,format=raw,cache=none,aio=native,detect-zeroes=on -device virtio-blk-pci,drive=drive-virtio1,id=virtio1,bus=pci.0,addr=0xb -netdev type=tap,id=net0,ifname=tap101i0,script=/var/lib/qemu-server/pve-bridge,downscript=/var/lib/qemu-server/pve-bridgedown -device e1000,mac=82:5B:E9:79:60:23,netdev=net0,bus=pci.0,addr=0x12,id=net0,bootindex=300 -rtc driftfix=slew,base=localtime -machine type=q35 -global kvm-pit.lost_tick_policy=discard
```

参考：

https://forums.unraid.net/topic/41951-gpu-passthrough-with-only-one-card/

## 硬件！！硬件！！

最大的阻碍是硬件，比如要让两个显卡同时运作，H77是做不到的，而Z77就可以，因为有多路原生PCIe。



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

