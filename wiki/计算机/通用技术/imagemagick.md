https://www.imagemagick.org/

imagemagick是个用于处理图像的命令行工具：

```
使用ImageMagick的创建，编辑，撰写，或转换位图图像。它可以读取和写入各种格式（超过200种）的图像，包括PNG，JPEG，GIF，HEIC，TIFF，DPX，EXR，WebP，Postscript，PDF和SVG。使用ImageMagick可以调整图像大小，翻转，镜像，旋转，变形，剪切和变换图像，调整图像颜色，应用各种特殊效果或绘制文本，线条，多边形，椭圆和贝塞尔曲线。
```

## 用 image magick 转换 pdf 到图片（拆分pdf）

> refer: https://jdhao.github.io/2019/11/20/convert_pdf_to_image_imagemagick/

将0到5页转换为图片，DPI为150，jpg质量为90：

```
$ convert -density 150 'scons-api.pdf[0-5]' -quality 90 output.jpg
```

## 用 image magick 转换图片到pdf

> refer: [imagemagick - convert images to pdf - Ask Ubuntu](https://askubuntu.com/quiestions/493584/convert-images-to-pdf)

```
$ convert "*.{png,jpg}" -quality 100 outfile.pdf
```

## 遇到的问题

```
convert: attempt to perform an operation not allowed by the security policy `gs' @ error/delegate.c/ExternalDelegateCommand/382.
```

修改`/etc/ImageMagick-7/policy.xml`，修改：

```
<!-- <policy domain="delegate" rights="none" pattern="gs" /> -->
```
