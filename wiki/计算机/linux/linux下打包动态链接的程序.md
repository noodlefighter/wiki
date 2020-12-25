## linux下打包动态链接的程序

要点：

- 带上需要的动态库（.so）
- 使用足够低版本的glibc

一个简单打包脚本，`script/do_pack.sh`：

```
#!/bin/bash

PROJ=protocol-test

SCRIPT_DIR=$(cd "$(dirname "$0")";pwd)
SRC_DIR="$SCRIPT_DIR/.."
BUILD_DIR="$PWD/build"
GIT_VER=$(git -C $SRC_DIR rev-parse --short HEAD)
PACK_NAME="${PROJ}-${GIT_VER}"
PACK_DIR="$BUILD_DIR/${PACK_NAME}"

copy_lib () {
        LibDir=$2
        Target=$1
        lib_array=($(ldd $Target | grep -o "/.*" | grep -o "/.*/[^[:space:]]*"))
        $(mkdir -p $LibDir)
        for Variable in ${lib_array[@]}
        do
            cp -vf "$Variable" "$LibDir"
        done
}

echo 准备环境...
rm -r "$BUILD_DIR"
mkdir -p "$BUILD_DIR" "$PACK_DIR"

echo 编译...
mkdir "$BUILD_DIR/bin" && cd "$BUILD_DIR/bin"
qmake "$SRC_DIR"
make -j16
cp "$PROJ" "$PACK_DIR/_$PROJ"
cp -vf "$SCRIPT_DIR/_run_packed_proj.sh" "$PACK_DIR/$PROJ"


# 删除glibc相关文件，使用目标系统上的GLIBC
# 由于GLIBC向前兼容，请在GLIBC较老的Linux版本上编译以获得最大兼容
echo 加入依赖库...
copy_lib "$BUILD_DIR/bin/${PROJ}" "$PACK_DIR"
cd $PACK_DIR
rm -rf libc.* libpthread.* ld-linux-* librt.*

echo 打包...
cd $PACK_DIR/..
cp -vf $SRC_DIR/res/* "$PACK_DIR"
tar -czvf "$PACK_NAME.tar.gz" "${PACK_NAME}"
```

`script/_run_packed_proj.sh`：

```
#!/bin/sh
appname=`basename $0 | sed s,\.sh$,,`
dirname=`dirname $0`
tmp="${dirname#?}"
if [ "${dirname%$tmp}" != "/" ]; then
dirname=$PWD/$dirname
fi
LD_LIBRARY_PATH=$dirname
export LD_LIBRARY_PATH
$dirname/_$appname "$@"
```

一般还会使用patchelf把依赖的动态库的路径改了，这里没做，可能会有无法使用的情况。