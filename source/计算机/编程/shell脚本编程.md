

---



## 获取脚本所在目录

获取脚本所在路径, 而不是$PWD

```
SHELL_DIR=$(cd "$(dirname "$0")";pwd)
cd $SHELL_DIR
```

