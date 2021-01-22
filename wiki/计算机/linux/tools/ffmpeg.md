

## 使用ffmpeg转换音频视频格式

查看支持的格式：

```
-decoders           show available decoders
-encoders           show available encoders
```

音频转换示例，wave转adpcm：

```
$ ffmpeg -i StarWars60.wav  -f wav -acodec adpcm_ms StarWars60-adpcm.wav
```

