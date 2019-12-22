title: win10ltsb
date: 2019-06-15
categories:
- 计算机
- windows




---



## 下载安装

> via: <https://www.reddit.com/r/Piracy/comments/8pfnun/how_to_download_and_install_windows_10_ltsb/>

Unfortunately you can't upgrade from Windows 7/8/8.1 and normal Windows 10 editions (Home/Pro/Enterprise) to Enterprise LTSC 2019. You need to install it fresh. You can only upgrade from Enterprise LTSB 2016 to Enterprise LTSC 2019 and keep your programs and files.

- Step 1: Navigate to the s1ave77s SVF ISO converter tool GitLab page: <https://gitlab.com/s1ave77/SVF.ISO.CONVERTER>. Click on the small cloud icon and choose download zip. It should look like [this.](https://i.imgur.com/8DvE9yw.jpg)
- Step 2: Extract the downloaded zip file using a program like 7-zip.
- Step 3: Run svf.iso.converter.aio.cmd from the extracted folder. When the command prompt window is open: Type "M" to open the Visual Studio Downloads page (misleading I know) and then type "7" to start the LTSC 2019 Process. Follow the on-screen prompts such as your PC's architecture, and language. I typed "6" to select the 64bit architecture and then I typed "0" and "8" to select the English (United States) language.

The program will automatically download the latest Evaluation ISO from Microsoft's servers and then convert it to a proper ISO of Windows 10 LTSC 2019.

**IMPORTANT**: Once the process is done you will have two different iso files in the same folder as svf.iso.converter. One will be called "en_windows_10_enterprise_ltsc_2019_x64_dvd_74865958".

(For 32-bit versions you want to use en_windows_10_enterprise_ltsc_2019_x86_dvd_97449f83)

**DO NOT USE THE ISO THAT STARTS WITH "17763.1.180914-1434.rs5".** This is the evaluation ISO that cannot be activated. The ISO name includes capital letters and has the phrase "EVAL" in the name. You will want to use the ISO that uses lower case names.



How do you activate?

Check out this guide on HWIDGen, created by s1ave77

<https://www.reddit.com/r/sjain_guides/comments/9qyuij/hwidkms38genmk6_download_and_usage_guide/>

When running the tool, change the Work Mode to KMS38 instead of HWID.