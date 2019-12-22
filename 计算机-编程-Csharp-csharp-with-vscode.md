title: csharp-with-vscode
date: 2019-09-24
categories:
- 计算机
- 编程
- Csharp




---



## .Net Core项目

MS在开源社区上的努力成功之一，早几年尝试过Mono Project但问题比较多只是个玩具，但现在官方在跨平台上发力了。



## dotnet cli

dotnet命令行工具。帮助文档：

https://docs.microsoft.com/en-us/dotnet/core/tools/?tabs=netcore2x



如：

```
# 新建解决方案：
dotnet new sln
# 将工程加入解决方案
dotnet sln add <project-path>
```



## vscode中使用C#

使用一个`OmniSharp`插件即可.



### 遇到的问题

#### "OmniSharp could not find the 'Microsoft.NET.Sdk' thing."

Please add this two files to the package:

/etc/profile.d/dotnet.sh

```
export DOTNET_ROOT=/opt/dotnet
export MSBuildSDKsPath=$DOTNET_ROOT/sdk/$(${DOTNET_ROOT}/dotnet --version)/Sdks
export PATH=${PATH}:${DOTNET_ROOT}
```

/etc/profile.d/dotnet.csh
```
setenv DOTNET_ROOT="/opt/dotnet"
setenv MSBuildSDKsPath="${DOTNET_ROOT}/sdk/$(${DOTNET_ROOT}/dotnet --version)/Sdks"
setenv PATH="${PATH}:${DOTNET_ROOT}"
```



## MSBuild构建相关

用Visual Studio时并不需要关心构建，但使用dotnet cli就有可能需要修改构建文件。

文件格式：

https://docs.microsoft.com/zh-cn/visualstudio/msbuild/msbuild-project-file-schema-reference?view=vs-2019

dotnet中对MSBuild增加的部分：

https://docs.microsoft.com/zh-cn/dotnet/core/tools/csproj



## Release

发布：

```
dotnet publish -r win-x64 -c release
```



.Net Core 3.0支持将程序打包成小体积的单个二进制文件：

https://www.hanselman.com/blog/MakingATinyNETCore30EntirelySelfcontainedSingleExecutable.aspx