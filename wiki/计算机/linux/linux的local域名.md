

当局域网中存在一台hostname为aaa的计算机，不管它是Windows还是Linux（一般得是桌面OS），用aaa.local可以找到它，这是mDNS提供的功能，可以参考wikipediahttps://en.wikipedia.org/wiki/.local

## Linux中开启avahi以使用.local域名

debian系下的包为`avahi-utils`，Arch系是`avahi`