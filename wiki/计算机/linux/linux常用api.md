---

## unistd.h 

usleep()

mkstemp() 创建临时文件

### POSIX的fsync/sync等命令的区别

> via: https://stackoverflow.com/questions/48171855/what-is-the-difference-between-fsync-and-syncfs
>
> 1. POSIX `fsync()`: "please write data for this file to disk"
> 2. POSIX `sync()`: "write all data to disk when you get around to it"
> 3. Linux `sync()`: "write all data to disk (when you get around to it?)"
> 4. Linux `syncfs()`: "write all data for the filesystem associated with this file to disk (when you get around to it?)"
> 5. Linux `fsync()`: "write all data and metadata for this file to disk, and don't return until you do"
