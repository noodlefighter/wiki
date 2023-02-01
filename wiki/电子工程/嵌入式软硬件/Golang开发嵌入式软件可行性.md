---



> TODO: 

Golang适合快速开发，有GC不用自己管理内存，能优雅地和C/C++混编。但它的runtime似乎没实时性保证，因为垃圾回收机制可能会`Stop The World`，这里研究一下可行性。




https://github.com/rakyll/go-hardware

https://embd.kidoman.io/

https://qiita.com/tetsu_koba/items/7435ef8d0c77844d751e

https://studygolang.com/articles/11904

https://blog.csdn.net/qq_15427331/article/details/54613635

https://www.zhihu.com/question/21615032/answers/created

https://golang.org/doc/go1.10

https://blog.cloudflare.com/recycling-memory-buffers-in-go/

https://postd.cc/why-go-is-not-good/

http://blog.kmckk.com/archives/2712814.html

https://mender.io/blog/why-did-we-choose-golang-over-c

golang问题最大还是GC，即使不断优化，但还是用着老旧的算法，我们只能减少频繁创建对象，减轻GC的负担。

选用这种语言，很多时候是想利用他现成的库，如果那些库在设计的时候没这方面考量，那在嵌入式场合可能就不能直接拿来用（如果有go的嵌入式社区，可能又是另外一番景象了）

## golang交叉编译测试

**helloworld**

```
$ cat helloworld.go
package main
import (
  "fmt"
  "time"
)

func main() {
    fmt.Println("hello world")
    time.Sleep(200 * 1000 * time.Millisecond)
}
$ env GOOS=linux GOARCH=arm go build -a -gcflags=all="-B" -ldflags="-w -s" helloworld.go
$ ls -lah helloworld
-rwxr-xr-x 1 r r 1.3M 12月 7日 10:16 helloworld
```

板上运行

```
# cat /proc/4261/status
Name:	helloworld
State:	S (sleeping)
Tgid:	4261
Ngid:	0
Pid:	4261
PPid:	4254
TracerPid:	0
Uid:	0	0	0	0
Gid:	0	0	0	0
FDSize:	256
Groups:	0
VmPeak:	  794956 kB
VmSize:	  794956 kB
VmLck:	       0 kB
VmPin:	       0 kB
VmHWM:	    1292 kB
VmRSS:	    1292 kB
VmData:	  793660 kB
VmStk:	     136 kB
VmExe:	     560 kB
VmLib:	       0 kB
VmPTE:	      12 kB
VmPMD:	       0 kB
VmSwap:	       0 kB
Threads:	4
```

**simple-rtsp-server**（https://github.com/aler9/rtsp-simple-server/tree/v0.20.2）

```
$ env GOOS=linux GOARCH=arm go build -ldflags="-extldflags=-static -s" -gcflags=all=-l -o rtsp-simple-server_arm
$ ls -lah rtsp-simple-server_arm
-rwxr-xr-x 1 r r 12M 12月 7日 11:16 rtsp-simple-server_arm
$ upx ./rtsp-simple-server_arm
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2022
UPX git-fdec47  Markus Oberhumer, Laszlo Molnar & John Reiser   Nov 16th 2022

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
  11796480 ->   4100684   34.76%    linux/arm    rtsp-simple-server_arm

Packed 1 file.

WARNING: this is an unstable beta version - use for testing only! Really.
```

编译后12M，upx后4M。板上运行：

```
# cat /proc/4395/status
Name:	rtsp-simple-ser
State:	S (sleeping)
Tgid:	4395
Ngid:	0
Pid:	4395
PPid:	615
TracerPid:	0
Uid:	0	0	0	0
Gid:	0	0	0	0
FDSize:	256
Groups:	0
VmPeak:	  806444 kB
VmSize:	  806444 kB
VmLck:	       0 kB
VmPin:	       0 kB
VmHWM:	   15780 kB
VmRSS:	   15780 kB
VmData:	  806176 kB
VmStk:	     264 kB
VmExe:	   15656 kB
VmLib:	4294951640 kB
VmPTE:	      30 kB
VmPMD:	       0 kB
VmSwap:	       0 kB
Threads:	8
```

VmSize莫名地大，可能是runtime开了一大片heap区域。
