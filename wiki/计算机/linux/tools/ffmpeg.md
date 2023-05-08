

## 使用ffmpeg转换音频视频格式

> 参数：http://www.ffmpeg.org/ffmpeg-all.html

查看支持的格式：

```
-decoders           show available decoders
-encoders           show available encoders
```

音频转换示例：

```
wav转adpcm:
ffmpeg -i test.wav  -f wav -acodec adpcm_ms test-adpcm.wav
mp3转wav:
ffmpeg -f mp3 -i test.mp3 test.wav
```

截取：

```
ffmpeg -i input.wav -ss 00:00:05 -t 00:00:10 -c copy output.wav
```

常用参数：

```
-ac 1 设置声道数为1
-ar 48000 设置采样率为48000Hz
例： ffmpeg -f mp3 -i kukou.mp3 -ac 1 -ar 22050 kukou-22050-mono.mp3
```



## ffmpeg提取mkv的音视频

先用ffprobe看mkv里内封的数据：

```
$ ffprobe example.mkv
...
[matroska,webm @ 0x5577e6f52fc0] Invalid value of WAVEFORMATEXTENSIBLE_CHANNEL_MASK
Input #0, matroska,webm, from 'example.mkv':
  Metadata:
    encoder         : libebml v1.3.6 + libmatroska v1.4.9
    creation_time   : 2019-03-20T21:31:04.000000Z
  Duration: 00:13:22.97, start: 0.000000, bitrate: 6416 kb/s
  Stream #0:0: Video: hevc (Main 10), yuv420p10le(tv, bt709), 1280x720 [SAR 1:1 DAR 16:9], 23.98 fps, 23.98 tbr, 1k tbn (default)
    Metadata:
      title           : [HQR] Asobi Asobase OVA
      BPS-eng         : 5665347
      DURATION-eng    : 00:13:22.969000000
      NUMBER_OF_FRAMES-eng: 19252
      NUMBER_OF_BYTES-eng: 568637349
      _STATISTICS_WRITING_APP-eng: mkvmerge v31.0.0 ('Dolores In A Shoestand') 32-bit
      _STATISTICS_WRITING_DATE_UTC-eng: 2019-03-20 21:31:04
      _STATISTICS_TAGS-eng: BPS DURATION NUMBER_OF_FRAMES NUMBER_OF_BYTES
  Stream #0:1(jpn): Audio: flac, 48000 Hz, stereo, s16 (default)
    Metadata:
      title           : Original
      BPS-eng         : 749053
      DURATION-eng    : 00:13:22.749000000
      NUMBER_OF_FRAMES-eng: 9408
      NUMBER_OF_BYTES-eng: 75162732
      _STATISTICS_WRITING_APP-eng: mkvmerge v31.0.0 ('Dolores In A Shoestand') 32-bit
      _STATISTICS_WRITING_DATE_UTC-eng: 2019-03-20 21:31:04
      _STATISTICS_TAGS-eng: BPS DURATION NUMBER_OF_FRAMES NUMBER_OF_BYTES
```

提取：

```
$ ffmpeg -i example.mkv -map 0:0 -acodec copy video.mp4
$ ffmpeg -i example.mkv -map 0:1 -acodec copy audio.flac
```



## ffmpeg生成ts流，ffmpeg提取ts流中的音视频

生成72Mbit/s的流：

```
$ ffmpeg \
  -i video.mp4 -i audio.flac \
  -i video.mp4 -i audio.flac \
  -map 0:0 -map 1:0 \
  -map 2:0 -map 3:0 \
  -program title=Prog0:st=0:st=1 \
  -program title=Prog1:st=2:st=3 \
  -f mpegts -muxrate 72000000 \
  mpts.ts
```

提取：

```
# ffmpeg -i mpts.ts -map 0:1 -acodec copy test.mp2
Input #0, mpegts, from 'mpts.ts':
  Duration: 00:00:11.65, start: 1.431689, bitrate: 71689 kb/s
  Program 1
    Metadata:
      service_name    : Prog0
      service_provider: FFmpeg
  Stream #0:0[0x100]: Video: mpeg2video (Main) ([2][0][0][0] / 0x0002), yuv420p(tv, bt709, progressive), 1280x720 [SAR 1:1 DAR 16:9], 23.98 fps, 23.98 tbr, 90k tbn, 47.95 tbc
    Side data:
      cpb: bitrate max/min/avg: 0/0/0 buffer size: 49152 vbv_delay: N/A
  Stream #0:1[0x101]: Audio: mp2 ([3][0][0][0] / 0x0003), 48000 Hz, stereo, fltp, 384 kb/s
  Program 2
    Metadata:
      service_name    : Prog1
      service_provider: FFmpeg
  Stream #0:2[0x102]: Video: mpeg2video (Main) ([2][0][0][0] / 0x0002), yuv420p(tv, bt709, progressive), 1280x720 [SAR 1:1 DAR 16:9], 23.98 fps, 23.98 tbr, 90k tbn, 47.95 tbc
    Side data:
      cpb: bitrate max/min/avg: 0/0/0 buffer size: 49152 vbv_delay: N/A
  Stream #0:3[0x103]: Audio: mp2 ([3][0][0][0] / 0x0003), 48000 Hz, stereo, s16p, 384 kb/s
Output #0, mp2, to 'test.mp2':
  Metadata:
    encoder         : Lavf58.76.100
  Stream #0:0: Audio: mp2 ([3][0][0][0] / 0x0003), 48000 Hz, stereo, fltp, 384 kb/s
Stream mapping:
  Stream #0:1 -> #0:0 (copy)
Press [q] to stop, [?] for help
size=     540kB time=00:00:11.49 bitrate= 384.8kbits/s speed=15.6x
video:0kB audio:540kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.000000%
```



