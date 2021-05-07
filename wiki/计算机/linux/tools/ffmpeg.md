

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

