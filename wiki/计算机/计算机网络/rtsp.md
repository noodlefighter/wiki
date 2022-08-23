

---



参考：

[从零开始写一个发送h264的rtsp服务器](https://www.cnblogs.com/x_wukong/p/8603480.html)

## RTSP协议文档

RFC2326：https://www.ietf.org/rfc/rfc2326.txt

## h264

paser分析器：https://sourceforge.net/projects/h264streamanalysis/

规范文档：

Information technology -- Coding of audio-visual objects -- Part 10: Advanced Video Coding

[ISO/IEC 14496-10:2014](https://standards.iso.org/ittf/PubliclyAvailableStandards/c066069_ISO_IEC_14496-10_2014.zip)



## 临时RTSP服务器架设

推和拉都是同一个端口

```
$ docker run -it -p 8554:8554 aler9/rtsp-simple-server

MP3推RTSP流
$ ffmpeg -re -stream_loop -1 -i 01-Skyfall.flac -vn -c:a libmp3lame -rtsp_transport tcp -f rtsp rtsp://localhost:8554/aaaa.rdp

拉流
$ ffplay rtsp://localhost:8554/aaaa.rdp

```


