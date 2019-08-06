

---



## 使用openssl进行aes加密、解密

```
$ openssl aes-128-cbc -K `xxd -p ../base_key.bin` -iv `xxd -p ../base_key_vi.bin` -e -in aes_256_src_buf.bin > aes_256_src_buf-encrypt.bin
```

```
$ openssl aes-128-cbc -K `xxd -p ../base_key.bin` -iv `xxd -p ../base_key_vi.bin` -d -in aes_256_src_buf-encrypt.bin > aes_256_src_buf-decrypt.bin
```

-K为key，-iv为IV，-e为encrypt，-d为解密，-in为文件输入

## 随机生成若干位的key

32位，base64格式：

```
$ openssl rand -base64 32 > key.bin
```

## RSA

openssh格式key转pem：

```
$ openssl rsa -in id_rsa -outform pem > id_rsa.pem
$ openssl rsa -in id_rsa -pubout -outform pem > id_rsa.pub.pem
```

生成pem格式s公/私钥：

```
$ openssl genrsa -out key.pem 2048
$ openssl rsa -in key.pem -pubout -outform pem > key.pub.pem
```

加密解密：

```
公钥加密
$ openssl rsautl -encrypt -inkey key.pub.pem -pubin -in data.bin -out data.bin.enc

私钥解密
$ openssl rsautl -decrypt -inkey key.pem -in data.bin.en -out data.bin

私钥加密
$ openssl rsautl -sign -inkey key.pem -in data.bin -out data.bin.sign

公钥解密
$ openssl rsautl -verify -inkey key.pub.pem -pubin -in data.bin.sign -out data.bin
```


> 公钥加密后的数据，要用私钥解密；私钥加密后的数据，要用公钥解密；但由于私钥包含公钥信息，所以实际上都能解

遇到了个坑，使用私钥加密出来的密文，无法用公钥解密：

```
这里以为用了私钥加密，但实际上openssl会自动帮你用公钥加密。。
$ openssl rsautl -encrypt -inkey key.pem -in data.bin -out data.bin.enc

所以当用这条，进行公钥解密时，会报错。。而用私钥就能解
$ openssl rsautl -decrypt -inkey key.pub.pem -pubin -in data.bin.enc -out data.bin
```


## 打印rsa密钥

```
$ openssl rsa -in key.pem -text -noout
```

对应到RSA密钥里的项：

```
modulus  N项
publicExponent E项
privateExponent D项
prime1 
prime2
exponent1
exponent2
coefficient
```


## 如何用openssl加密一个大文件

> via: https://www.czeskis.com/random/openssl-encrypt-file.html

#### Step 0) Get their public key

The other person needs to send you their public key in .pem format. If they only have it in rsa format (*e.g.*, they use it for ssh), then have them do:

```
openssl rsa -in id_rsa -outform pem > id_rsa.pem

openssl rsa -in id_rsa -pubout -outform pem > id_rsa.pub.pem
```

Have them send you *id_rsa.pub.pem*

#### Step 1) Generate a 256 bit (32 byte) random key

```
openssl rand -base64 32 > key.bin
```

#### Step 2) Encrypt the key

```
openssl rsautl -encrypt -inkey id_rsa.pub.pem -pubin -in key.bin -out key.bin.enc
```


#### Step 3) Actually Encrypt our large file

```
openssl enc -aes-256-cbc -salt -in SECRET_FILE -out SECRET_FILE.enc -pass file:./key.bin
```


#### Step 4) Send/Decrypt the files

Send the *.enc* files to the other person and have them do:

```
openssl rsautl -decrypt -inkey id_rsa.pem -in key.bin.enc -out key.bin 

openssl enc -d -aes-256-cbc -in SECRET_FILE.enc -out SECRET_FILE -pass file:./key.bin
```


#### Notes

You should **always** verify the hash of the file with the recipient or sign it with your private key, so the other person knows it actually came from you.

If there is a man-in-the-middle, then he/she could substitute the other person's public key for his/her own and then you're screwed. **Always** verify the other person's public key (take a hash and read it to each other over the phone).


## 证书相关

参考： https://www.cnblogs.com/osbreak/p/9486188.html