title: pid-file
date: 2019-09-06
categories:
- 计算机
- linux
- userspace


---

> via: http://vinllen.com/pid-filehe-jin-cheng-fu-ben/

## 1.如何防止启动多个副本

  为了防止启动一个进程的多个副本，需要在写的时候申请文件锁，一个进程一旦申请文件锁后，会一直锁住该pid文件，直到进程退出，这样也就达到了只启动一个副本的目的。
  实例代码如下：

```
const string LOCKFILE = "/var/run/agent.pid";  
const mode_t LOCKMOD = (S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);

int  
lockfile (int fd) {  
    struct flock fl;

    fl.l_type = F_WRLCK;
    fl.l_start = 0;
    fl.l_whence = SEEK_SET;
    fl.l_len = 0;
    return fcntl(fd, F_SETLK, &fl);
}

int  
already_running() {  
    int fd;
    char buf[16];

    fd = open(LOCKFILE.c_str(), O_RDWR | O_CREAT, LOCKMOD);
    if (fd < 0) {
        printf("ERROR: cann't open pid file: %s\n", LOCKFILE.c_str());
        return -1;
    }
    if (lockfile(fd) < 0) {
        if (errno == EACCES || errno == EAGAIN) {
            close(fd);
            printf("WARNING: process already run\n");
            return 0;
        }
        printf("ERROR: cann't lock pid file: %s error: %s\n", LOCKFILE.c_str(), strerror(errno));
        return -2;
    }
    ftruncate(fd, 0);
    stringstream ss;
    ss << getpid() << endl;
    string tmps = ss.str();
    write(fd, tmps.c_str(), tmps.size());
    return 1;
}

int main () {  
    if (already_running() <= 0) {
        return 0;
    }
    //...
}
```

## 2.如何保证在进程挂掉后把进程重新启动

  pid file的功能做不到这一点。此时，我们需要搞一个脚本检测pid file，如果读取文件为空，则进程肯定没启动，再执行启动就OK。那么，万一读取文件不为空呢？上一个进程退出后没法删除pid file中的进程号（当然，理论上也可以做到，只是比较麻烦：析构函数进行删除，同时注册信号量响应函数，响应各种异常退出的信号量进行pid file的删除）。一种比较简单的方法是发送kill -0 $pid命令，$pid是读取出来的pid号。如果返回值$?为0表示进程存在，否则表示不存在，重新启动即可。ps:注意一下权限。
  脚本实例如下：

```
#!/bin/sh

pid_file="/var/run/agent.pid"  
sleep_time="20s"

while [ 1 -eq 1 ]  
do  
    if [ ! -f $pid_file ]
    then
        echo "agent pid file not exist"
        /home/xxx/agent &
        sleep $sleep_time
        continue
    fi

    pid=`cat $pid_file`
    kill -0 $pid
    if [ $? -ne 0 ]
    then
        echo "agent process not exist"
        /home/xxx/agent &
    fi

    sleep $sleep_time
done  
```