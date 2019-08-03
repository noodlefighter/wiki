

---



## 使用openssl进行aes加密、解密



```
$ openssl aes-128-cbc -K `xxd -p ../base_key.bin` -iv `xxd -p ../base_key_vi.bin` -e -in aes_256_src_buf.bin > aes_256_src_buf-encrypt.bin
```

```
$ openssl aes-128-cbc -K `xxd -p ../base_key.bin` -iv `xxd -p ../base_key_vi.bin` -d -in aes_256_src_buf-encrypt.bin > aes_256_src_buf-decrypt.bin
```

-K为key，-iv为IV，-e为encrypt，-d为解密，-in为文件输入

