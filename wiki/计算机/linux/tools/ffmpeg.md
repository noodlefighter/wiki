

## 使用ffmpeg转换音频视频格式

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
ffmpeg -i input.wav -ss 00:00:05 -t 00:00:10 output.wav
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



