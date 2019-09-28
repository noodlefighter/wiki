

---



介绍：

https://www.cnblogs.com/shenhaocn/archive/2011/04/11/2013112.html

https://www.embeddedlinux.org.cn/emb-linux/kernel-driver/201710/25-7674.html

官方：

http://www.linux-fbdev.org/HOWTO/index.html





```
inf fdScreen = open( "devicename", O_RDWR );
fb_var_screeninfo varInfo;
ioctl( fdScreen, FBIOGET_VSCREENINFO, &varInfo );

//set resolution/dpi/color depth/.. in varInfo, then write it back
ioctl( fdScreen, FBIOPUT_VSCREENINFO, &varInfo );

//get writable screen memory; unsigned short here for 16bit color
unsigned short* display = mmap( 0, nScreenSize,
                                PROT_READ | PROT_WRITE, MAP_SHARED, fdScreen, 0 );
```

