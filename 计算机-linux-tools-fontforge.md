title: fontforge
date: 2019-09-30
categories:
- 计算机
- linux
- tools




---

## 使用fontforge解压ttc字体到ttf/otf字体

ttc是被推荐使用的新格式，其中可以包含多个ttf/otf字体，他们可以有一些公用部分，所以整体大小比分开的几个字体文件更小。

> via: https://gist.github.com/fatum12/941a10f31ac1ad48ccbc

```
#!/usr/local/bin/fontforge
# Usage: fontforge -script ttc2ttf.pe /path/to/font.ttc

fonts = FontsInFile($1)
n = SizeOf(fonts)
i = 0
while (i < n)
    Open($1 + "(" + fonts[i] + ")", 1)

    ext = ".ttf"
    if ($order == 3)
        ext = ".otf"
    endif

    filename = $fontname + ext
    Generate(filename)
    Print(filename)
    Close()
    ++i
endloop
```

> TODO: 试了一下好像不顶用啊。。有空再试试