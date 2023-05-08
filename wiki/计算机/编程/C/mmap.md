

## mmap+memcpy删除文件头部一段数据

```
    int fd = open(up_filename.c_str(), O_RDWR);
    void *ptr = mmap(NULL, file_len , PROT_READ|PROT_WRITE, MAP_SHARED , fd , 0);
    memcpy(ptr, ptr + 32, file_len - 32);
    ftruncate(fd, file_len - 32);
    close(fd);
```

