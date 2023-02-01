

---



## 取程序运行路径路径

golang，执行路径

```
import (
	"path/filepath"
	"strings"
)

func getCurrentDirectory() string {
    dir, err := filepath.Abs(filepath.Dir(os.Args[0]))
    if err != nil {
        return ""
    }
    return strings.Replace(dir, "\\", "/", -1)
}
```

要注意用`go run`的方式启动时，该方法拿不到正确的路径，因为它帮我们编译到了临时目录里。

## 日志

> via: <https://my.oschina.net/robin3d/blog/1862755>

```
package main

import (
	"log"
	"os"
)

var logger *log.Logger

func main() {
	file, err := os.OpenFile("test.log", os.O_APPEND|os.O_CREATE, 666)
	if err != nil {
		log.Fatalln("fail to create test.log file!")
	}
	defer file.Close()
	logger = log.New(file, "", log.LstdFlags|log.Lshortfile) // 日志文件格式:log包含时间及文件行数
	log.Println("输出日志到命令行终端")
	logger.Println("将日志写入文件")

	logger.SetFlags(log.LstdFlags | log.Lshortfile) // 设置日志格式

	log.Panicln("在命令行终端输出panic，并中断程序执行")
	logger.Panicln("在日志文件中写入panic，并中断程序执行")

	log.Fatal("在命令行终端输出日志并执行os.exit(1)")
	logger.Fatal("在日志文件中写入日志并执行os.exit(1)")
}
```

## 判断文件是否存在

```
func PathExists(path string) (bool, error) {
	_, err := os.Stat(path)
	if err == nil {
		return true, nil
	}
	if os.IsNotExist(err) {
		return false, nil
	}
	return false, err
}
```

## 在go中执行命令

> via: <https://stackoverflow.com/questions/6182369/exec-a-shell-command-in-go>

```
package main

import (
    "bytes"
    "fmt"
    "log"
    "os/exec"
)

const ShellToUse = "bash"

func Shellout(command string) (error, string, string) {
    var stdout bytes.Buffer
    var stderr bytes.Buffer
    cmd := exec.Command(ShellToUse, "-c", command)
    cmd.Stdout = &stdout
    cmd.Stderr = &stderr
    err := cmd.Run()
    return err, stdout.String(), stderr.String()
}

func main() {
    err, out, errout := Shellout("ls -ltr")
    if err != nil {
        log.Printf("error: %v\n", err)
    }
    fmt.Println("--- stdout ---")
    fmt.Println(out)
    fmt.Println("--- stderr ---")
    fmt.Println(errout)
}
```

直接输出到stdout上：

```
func Shellout(command string) (error) {
    //var stdout bytes.Buffer
    cmd := exec.Command(ShellToUse, "-c", command)
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stdout
    err := cmd.Run()
    return err
}
```

