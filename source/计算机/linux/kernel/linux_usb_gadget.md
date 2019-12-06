

---



## Linux USB Gadget

Linux下的USB从设备叫USB Gadget。

http://www.linux-usb.org/gadget/

https://www.kernel.org/doc/html/latest/driver-api/usb/gadget.html

https://www.kernel.org/doc/html/latest/usb/gadget_serial.html

https://www.kernel.org/doc/html/latest/usb/functionfs.html

使用gadgetfs创建自己的usb设备：

https://blog.soutade.fr/post/2016/07/create-your-own-usb-gadget-with-gadgetfs.html



## 如何用起现有gadget里的function

PPT，Make your own USB gadget：

https://events.static.linuxfound.org/sites/events/files/slides/LinuxConNA-Make-your-own-USB-gadget-Andrzej.Pietrasiewicz.pdf

gadget的configfs配置：

https://www.kernel.org/doc/Documentation/usb/gadget_configfs.txt



## 实现一个MTP Server（设备端）

http://www.trivialfeat.com/home/2016/11/17/media-transfer-protocol-in-a-usb-composite-gadget

文章中提到一个现成的kernel的patch。

文章备份：

```

## Options:

- ANDROID MTP

  :

  - https://android.googlesource.com/platform/frameworks/base/+/master/media/jni/
  - Apache 2.0 license.
  - Requires Android configfs MTP gadget module which is not in the Linux kernel.
  - Seems to be very closely tied to Android media code and require many other android libraries that I did not want to merge.

- TIZEN MTP

  :

  - https://build.tizen.org/package/show?package=mtp-responder&project=Tizen%3AIVI
  - Apache 2.0 license.
  - Requires GLIB 2.0 and some capi that would inflate our image size by a good bit.

- BUTEO MTP

  :

  - Current repo: https://git.merproject.org/mer-core/buteo-mtp/tree/master
  - Repo I used: https://github.com/pcercuei/buteo-mtp (Pcercuei already separated it from buteo-syncfw here, see next bullet)
  - Newer version of buteo is intrinsically tied to buteo-syncfw. buteo-syncfw requires many more platform code packages to be pulled in from the Meego or Mer code base. Since this added code handles config and networking etc, it was not very useful to me.
  - Buteo was originally written for gadgetfs and alot of the documentation still shows this. However, Buteo now uses functionfs gadget module with configfs. This adds to the confusion a bit.

- UBUNTU MTP

  :

  - http://bazaar.launchpad.net/~phablet-team/mtp/trunk/files
  - Requires Boost library with certain packages, dbus-cpp, libglog. Boost library will inflate our image size a good bit.
  - Also requires bazaar installed on the dev machine to pull from the Ubuntu repo.
  - Requires Android configfs MTP gadget module which is not in the Linux kernel.

- uMTP-Responder

  - https://github.com/viveris/uMTP-Responder
  - Thanks to Jean-François DEL NERO for the update on this.
  - Recently released by Viveris under GPLv3. (This is newer than the instructions here)
  - Implemented in C, in user space and use the GadgetFs layer.
  - This is most likely a better option than the instructions below. Give it a try!

## Implementation:

Note: There may be a better and more proper Linux way to implement MTP, but in the time frame I have, this was the fastest working way I found with existing code. It seems that good details are hard to find on MTP responders when you don't want to write your own.

I first began looking at buteo since it used functionfs which is already in the kernel. I was able to pull the old version and build it. Running the binary seemed to work, however attaching the gadget configuration to the UDC caused a kernel oops every time.

Ubuntu was the second flavor I tried and ultimately found success. Thank you Android and Canonical phablet team! Here's the steps and files necessary to pull Ubuntu's MTP daemon into a buildroot system:

**1. Pull down the kernel patch for the MTP gadget driver that was never accepted into the kernel. Add this to your build.**

1. https://patches.linaro.org/patch/52411/
2. Download from the patch link
3. cp RFC-1-2-usb-gadget-configfs-add-MTP-function.patch <your linux patches directory>

**2. Select the newly added MTP gadget option in the kernel config**

1. make linux-menuconfig
2. Device Drivers -> USB Support -> USB Gadget Support -> USB Gadget Drivers -> USB functions configurable through configfs
3. Select MTP gadget
4. Also select any others you want to use. I'm also selecting ACM serial and Mass Storage.
3. Save the configuration to your default config (optional)

make linux-savedefconfig
cp output/build/linux-linux4sam_5.3/defconfig <your defconfig location>
4. Setup ubuntu-mtp package in buildroot

cd <path to your package directory>
mkdir ubuntu-mtp
Add Config.in:
config BR2_PACKAGE_UBUNTU_MTP
    bool "ubuntu-mtp"
    select BR2_PACKAGE_BOOST
    select BR2_PACKAGE_BOOST_THREAD
    select BR2_PACKAGE_BOOST_SYSTEM
    select BR2_PACKAGE_BOOST_FILESYSTEM
    select BR2_PACKAGE_BOOST_TEST
    select BR2_PACKAGE_DBUS_CPP
    select BR2_PACKAGE_GLOG

    help
      Media Transfer Protocol (MTP) stack from Ubuntu
    
      http://bazaar.launchpad.net/~phablet-team/mtp

5. Add ubuntu-mtp.mk. Note that I am using sed to replace tags added in the patch file.

#############################################################
#
# Ubuntu MTP responder
# source http://bazaar.launchpad.net/~phablet-team/mtp/trunk
# Adding as a local package to avoid baazar requirement
#
#############################################################
UBUNTU_MTP_VERSION = 71
UBUNTU_MTP_SITE = file://$(TOPDIR)/Company/package/ubuntu-mtp
UBUNTU_MTP_DEPENDENCIES = boost dbus-cpp
UBUNTU_MTP_LICENSE = GPLv3
UBUNTU_MTP_LICENSE_FILES = COPYING
UBUNTU_MTP_INSTALL_STAGING = yes

define UBUNTU_MTP_SET_PROPERTIES
    $(SED) "s/---MANUFACTURER---/Company Name/" $(@D)/src/MtpServer.cpp
    $(SED) "s/---MODEL---/Product Name/" $(@D)/src/MtpServer.cpp
    $(SED) "s/---SERIAL---/Serial Number/" $(@D)/src/MtpServer.cpp
endef

UBUNTU_MTP_PRE_CONFIGURE_HOOKS += UBUNTU_MTP_SET_PROPERTIES

$(eval $(cmake-package))

6. Add patches to package directory. These patches strip out code that ties it to the ubuntu phablet and hard codes some config options. they also modify some build files to include libraries. Some assembly required here. Note you may want to modify these patch files to expose the proper disk locations. Currently, i'm exposing the /root partition for testing.

0001-CMake-remove-android-libraries-and-fix-module-names.patch
0002-remove-android-properties-and-ubuntu-phablet-specific.patch
0003-convert-android-properties-to-hardcoded-strings.patch
7. Pull down the MTP responder from the ubuntu bzr repo. Note: I saved the tgz to our repo so that bazaar is not a requirement for the build

Download the tarball here: http://bazaar.launchpad.net/~phablet-team/mtp/trunk/revision/71?start_revid=71
Add this to your ubuntu-mtp package directory
8. Package is done, add it to the top level Config.in

vim ../../Config.in
9. Select it in the menuconfig along with the dependencies and hope it builds

make menuconfig
User Provided Options
select ubuntu-mtp
10. After it builds and installs, create the gadget startup script. Simple example shown here. Also, get your own vid/pid ya bum!.

vim /etc/init.d/S99-gadget
#!/bin/sh

CONFIGFS="/sys/kernel/config"
GADGET="$CONFIGFS/usb_gadget"
VID="0x0000"
PID="0x0000"
SERIAL="0123456789"
MANUF="Me"
PRODUCT="Radget"

case "$1" in
    start)
        echo "Creating the USB gadget"

        echo "Loading composite module"
        modprobe libcomposite
    
        echo "Mounting ConfigFS"
        mount -t configfs none $CONFIGFS
        cd $GADGET
        if [ $? -ne 0 ]; then
            echo "Error setting up configfs"
            exit 1;
        fi
    
        echo "Creating gadget directory"
        mkdir gadget
        cd gadget
        if [ $? -ne 0 ]; then
            echo "Error creating usb gadget in configfs"
            exit 1;
        fi
    
        echo "Setting Vendor and Product ID's"
        echo $VID > idVendor
        echo $PID > idProduct
    
        echo "Setting English strings"
        mkdir strings/0x409
        echo $SERIAL > strings/0x409/serialnumber
        echo $MANUF > strings/0x409/manufacturer
        echo $PRODUCT > strings/0x409/product
    
        echo "Setting configuration"
        mkdir configs/c.1
        mkdir configs/c.1/strings/0x409
        echo "CDC ACM + MTP + Mass Storage" > configs/c.1/strings/0x409/configuration
        echo 120 > configs/c.1/MaxPower
    
        echo "Creating ACM interface"
        mkdir functions/acm.GS0
        ln -s functions/acm.GS0 configs/c.1
    
        echo "Creating MTP interface"
        mkdir functions/mtp.mtp
        ln -s functions/mtp.mtp configs/c.1
        mkdir /dev/mtp
        mount -t functionfs mtp /dev/mtp
    
        echo "Creating Mass Storage interface"  
        mkdir functions/mass_storage.ms0
        echo "/dev/mmcblk0" > functions/mass_storage.ms0/lun.0/file
        echo "1" > functions/mass_storage.ms0/lun.0/removable
        ln -s functions/mass_storage.ms0 configs/c.1/mass_storage.ms0
    
        echo "Binding USB Device Controller"
        echo `ls /sys/class/udc` > UDC
    
        echo "Starting the MTP responder daemon"
        mtp-server &
        ;;
    stop)
        echo "Stopping the USB gadget"
    
        echo "Killing MTP responder daemon"
        killall mtp-server
    
        cd $GADGET/gadget
    
        if [ $? -ne 0 ]; then
            echo "Error: no configfs gadget found" 
            exit 1;
        fi
    
        echo "Unbinding USB Device Controller"
        echo "" > UDC
    
        echo "Removing Mass Storage interface"
        rm configs/c.1/mass_storage.ms0
        rmdir functions/mass_storage.ms0
    
        echo "Removing MTP interface"
        umount /dev/mtp
        rmdir /dev/mtp
        rm configs/c.1/mtp.mtp
        rmdir functions/mtp.mtp
    
        echo "Removing ACM interface"
        rm configs/c.1/acm.GS0
        rmdir functions/acm.GS0
    
        echo "Clearing English strings"
        rmdir strings/0x409
    
        echo "Cleaning up configuration"
        rmdir configs/c.1/strings/0x409
        rmdir configs/c.1
    
        echo "Removing gadget directory"
        cd $GADGET
        rmdir gadget
    
        cd /
    
        echo "Unmounting ConfigFS"
        umount $CONFIGFS
        ;;
esac

11. The gadget should show up now when plugged in. Here's a quick screen cap of the directory structure showing the /root partition that i'm exposing.

```