

---



## 服务器配置：

```
# apt install nfs-kernel-server
# vi 
```

编辑配置`/etc/exports`：
```
/home/dev/workspaces/hi3516a/nfs        *(rw,sync,no_subtree_check)
```

挂载：
```
mount -t nfs localhost:/home/dev/workspaces/hi3516a/nfs /mnt/nfs
```

## 错误记录

```
svc: failed to register lockdv1 RPC service (errno 111)
加个-o nolock
```



## Arch Linux上的参考

https://wiki.archlinux.org/index.php/NFS



## windows上挂载NFS

* 先去“添加删除软件”那里开启nfs client功能

在cmd.exe下使用mount命令挂载（powershell不行，那里也有mount命令但不是nfs这个）：

```
mount 192.168.3.114:/root/nfsroot z:
```

注意，windows不支持UTF8挂载。

```
C:\Users\r>mount -o lang=UTF-8 192.168.3.114:/root/nfsroot z:
ERROR - Unrecognized lang type.

Use lang = euc-jp|euc-tw|euc-kr|shift-jis|big5|ksc5601|gb2312-80|ansi only
```

有人说这样能解决部分问题（“但是当接收别人平台发送的文件的时候，还是会出现乱码”，意思是会导致其他程序出问题？毕竟从习惯上都默认windows不使用utf8做文件名）：

![1561270766296](_assets/nfs/1561270766296.png)

## nfs选项描述

> via: https://www.thegeekdiary.com/common-nfs-mount-options-in-linux/

## rw (read/write) / ro (read-only)

– Use rw for data that users need to modify. In order for you to mount a directory read/write, the NFS server must export it read/write.
– Use ro for data you do not want users to change. A directory that is automounted from several servers should be read-only, to keep versions identical on all servers.
– the default is rw.

## suid / nosuid

– Specify suid if you want to allow mounted programs that have setuid permission to run with the permissions of their owners, regardless of who starts them. If a program with setuid permission is owned by root, it will run with root permissions, regardless of who starts it.
– Specify nosuid to protect your system against setuid programs that may run as root and damage your system.
– the default is suid.




## hard / soft

– Specify hard if users will be writing to the mounted directory or running programs located in it. When NFS tries to access a hard-mounted directory, it keeps trying until it succeeds or someone interrupts its attempts. If the server goes down, any processes using the mounted directory hang until the server comes back up and then continue processing without errors. Interruptible hard mounts may be interrupted with CTRL-C or kill (see the intr option, later).
– Specify soft if the server is unreliable and you want to prevent systems from hanging when the server is down. When NFS tries to access a soft-mounted directory, it gives up and returns an error message after trying retrans times (see the retrans option, later). Any processes using the mounted directory will return errors if the server goes down.
– Default is hard

## intr / nointr

– Specify intr if users are not likely to damage critical data by manually interrupting an NFS request. If a hard mount is interruptible, a user may press [CTRL]-C or issue the kill command to interrupt an NFS mount that is hanging indefinitely because a server is down.
– Specify nointr if users might damage critical data by manually interrupting an NFS request, and you would rather have the system hang while the server is down than risk losing data between the client and the server.
– The default is intr.

## fg (foreground) / bg (background)

– Specify fg for directories that are necessary for the client machine to boot or operate correctly. If a foreground mount fails, it is retried again in the foreground until it succeeds or is interrupted. All automounted directories are mounted in the foreground; you cannot specify the bg option with automounted directories.
– Specify bg for mounting directories that are not necessary for the client to boot or operate correctly. Background mounts that fail are re-tried in the background, allowing the mount process to consider the mount complete and go on to the next one. If you have two machines configured to mount directories from each other, configure the mounts on one of the machines as background mounts. That way, if both systems try to boot at once, they will not become deadlocked, each waiting to mount directories from the other. The bg option cannot be used with automounted directories.
– The default is fg.

## devs / nodevs

– Specify devs if you are mounting device files from a server whose device files will work correctly on the client. The devs option allows you to use NFS-mounted device files to read and write to devices from the NFS client. It is useful for maintaining a standard, centralized set of device files, if all your systems are configured similarly.
– Specify nodevs if device files mounted from a server will not work correctly for reading and writing to devices on the NFS client. The nodevs option generates an error if a process on the NFS client tries to read or write to an NFS-mounted device file.
– The default is devs.

## timeo=n

– The timeout, in tenths of a second, for NFS requests (read and write requests to mounted directories). If an NFS request times out, this timeout value is doubled, and the request is retransmitted. After the NFS request has been retransmitted the number of times specified by the retrans option (see below), a soft mount returns an error, and a hard mount retries the request. The maximum timeo value is 30 (3 seconds).
– Try doubling the timeo value if you see several servers not responding messages within a few minutes. This can happen because you are mounting directories across a gateway, because your server is slow, or because your network is busy with heavy traffic.
– Default is timeo=7

## retrans=n

– The number of times an NFS request (a read or write request to a mounted directory) is retransmitted after it times out. If the request does not succeed after n retransmissions, a soft mount returns an error, and a hard mount retries the request.
– Increase the retrans value for a directory that is soft-mounted from a server that has frequent, short periods of downtime. This gives the server sufficient time to recover, so the soft mount does not return an error.
– The default is retrans=4.

## retry=n

– The number of times the NFS client attempts to mount a directory after the first attempt fails. If you specify intr, you can interrupt the mount before n retries. However, if you specify nointr, you must wait until n retries have been made, until the mount succeeds, or until you reboot the system.
– If mounts are failing because your server is very busy, increasing the retry value may fix the problem.
– The default is retry=1.

## rsize=n

– The number of bytes the NFS client requests from the NFS server in a single read request.
– If packets are being dropped between the client and the server, decrease rsize to 4096 or 2048. To find out whether packets are being dropped, issue the “nfsstat -rc” command at the HP-UX prompt. If the timeout and retrans values returned by this command are high, but the badxid number is close to zero, then packets are being dropped somewhere in the network.
– The default is rsize=8192.

## wsize=n

– The number of bytes the NFS client sends to the NFS server in a single write request.
– If packets are being dropped between the client and the server, decrease wsize to 4096 or 2048. To find out whether packets are being dropped, issue the “nfsstat -rc” command at the HP-UX prompt. If the timeout and retrans values returned by this command are high, but the badxid number is close to zero, then packets are being dropped somewhere in the network.
– The default is wsize=8192.

## O (Overlay mount)

– Allows the file system to be mounted over an existing mount point, making the underlying file system inaccessible. If you attempt to mount a file system over an existing mount point without the -O option, the mount will fail with the error device busy.
– **Caution**: Using the -O mount option can put your system in a confusing state. The -O option allows you to hide local data under an NFS mount point without receiving any warning. Local data hidden beneath an NFS mount point will not be backed up during regular system backups.
– On HP-UX, the -O option is valid only for NFS-mounted file systems. For this reason, if you specify the -O option, you must also specify the -F nfs option to the mount command or the nfs file system type in the /etc/fstab file.
– The default value is not specified for the parameter.

## remount

– If the file system is mounted read-only, this option remounts it read/write. This allows you to change the access permissions from read-only to read/write without forcing everyone to leave the mounted directory or killing all processes using it.
– The Default value is not specified for this parameter.

## noac

– If specified, this option prevents the NFS client from caching attributes for the mounted directory.
– Specify noac for a directory that will be used frequently by many NFS clients. The noac option ensures that the file and directory attributes on the server are up to date, because no changes are cached on the clients. However, if many NFS clients using the same NFS server all disable attribute caching, the server may become overloaded with attribute requests and updates. You can also use the actimeo option to set all the caching timeouts to a small number of seconds, like 1 or 3.
– If you specify noac, do not specify the other caching options.
– The Default value is not specified for this parameter.

## nocto

– If specified, this option suppresses fresh attributes when opening a file.
– Specify nocto for a file or directory that never changes, to decrease the load on your network.
– The Default value is not specified for this parameter.

## acdirmax=n

– The maximum number of seconds a directory’s attributes are cached on the NFS client. When this timeout period expires, the client flushes its attribute cache, and if the attributes have changed, the client sends them to the NFS server.
– For a directory that rarely changes or that is owned and modified by only one user, like a user’s home directory, you can decrease the load on your network by setting acdirmax=120 or higher.
– The Default value is acdirmax=60.

## acdirmin=n

– The minimum number of seconds a directory’s attributes are cached on the NFS client. If the directory is modified before this timeout expires, the timeout period is extended by acdirmin seconds.
– For a directory that rarely changes or that is owned and modified by only one user, like a user’s home directory, you can decrease the load on your network by setting acdirmin=60 or higher.
– The Default value is acdirmin=30.

## acregmax=n

– The maximum number of seconds a file’s attributes are cached on the NFS client. When this timeout period expires, the client flushes its attribute cache, and if the attributes have changed, the client sends them to the NFS server.
– For a file that rarely changes or that is owned and modified by only one user, like a file in a user’s home directory, you can decrease the load on your network by setting acregmax=120 or higher.
– The Default value is acregmax=60.

## actimeo=n

– Setting actimeo to n seconds is equivalent to setting acdirmax, acdirmin, acregmax, and acregmin to n seconds.
– Set actimeo=1 or actimeo=3 for a directory that is used and modified frequently by many NFS clients. This ensures that the file and directory attributes are kept reasonably up to date, even if they are changed frequently from various client locations.
– Set actimeo=120 or higher for a directory that rarely or never changes.
– If you set the actimeo value, do not set the acdirmax, acdirmin, acregmax, or acregmin values.
– The default value is not set for this parameter.

## vers=n

– The version of the NFS protocol to use. By default, the local NFS client will attempt to mount the file system using NFS version 3. If the NFS server does not support version 3, the file system will be mounted using version 2.
– If you know that the NFS server does not support version 3, specify vers=2, and you will save time during the mount, because the client will not attempt to use version 3 before using version 2.
– The default value for the parameter is vers=3.

## grpid

– Forces a newly created file in the mounted file system to inherit the group ID of the parent directory.
– By default, a newly created file inherits the effective group ID of the calling process, unless the GID bit is set on the parent directory. If the GID bit is set, the new file inherits the group ID of the parent directory.
– The default value is not set for this parameter.