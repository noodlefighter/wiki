

---

## 加密解密

* 私钥包含公钥信息；

* 用公钥加密时，解密用私钥；用私钥加密时，解密用公钥；
* 由于密钥的不对称，即使泄漏了公钥，也无法与公钥持有者通讯。

RSA公钥包含{N, E}；RSA私钥包含{N, E, D}。

N模数(modules)，E幂(exponent)，D私有幂（private exponent）。

## 签名

私钥签名，公钥鉴签。

签名时，生成数据摘要（常见如sha256），用私钥对摘要加密，密文附在数据旁；鉴签时，生成数据摘要，公钥解密密文段，通过对比解密后的数据是否和摘要一致来判断签名有效性。

## RSA的填充（padding）

### 为什么RSA的padding是至关重要的？

> via: https://rdist.root.org/2009/10/06/why-rsa-encryption-padding-is-critical/

CRT can also be used to attack RSA. Consider an implementation that does not use any armoring. The encryption operation is simply the RSA primitive itself. A sender wants to send a message to three separate recipients. Thus, the sender calculates:

m^e mod A
m^e mod B
m^e mod C

The attacker can’t calculate the inverse of one of these encryptions directly because the eth root problem in each ring is difficult. However, because the message is the same for each recipient (but different ciphertexts), she can convert these operations into a group where the inverse operation is easy. To do this, she uses CRT to combine the three ciphertexts to get:

m^e mod A*B*C

Since m is smaller than each of A, B, and C, m^e is smaller than A*B*C if e=3. This means the attacker just has to calculate the cube root of the result, an operation that is easy in the monoid of integers modulo A*B*C. This is essentially an integer cube root, ordinary arithmetic. This shows why PKCS #1 armoring for encryption has always been randomized. It can be fatal to encrypt the same message multiple times, even to the same recipient. For signatures, it is more secure to randomize the padding as in RSASSA-PSS, but it is not yet fatal for legacy systems to continue to use PKCS #1 v1.5 signature padding, which is not randomized.

In public key crypto, padding is not an optional feature. It is a critical part of the cryptosystem security. The latest version of PKCS #1 (v2.1 as of this writing) should be used for both encryption/signing and decryption/verification. For new implementation, use the approaches that first appeared in v2.0 (RSAES-OAEP for encryption and RSASSA-PSS for signing). Failure to properly manage RSA armoring could allow attackers to forge signatures, decrypt ciphertext, or even recover your private key.


### RSA的填充方式

这是某个加密库里截出来的RSA填充方式列表：
```
SCHEME_NO_PADDING,            /**< without padding */
SCHEME_BLOCK_TYPE_0,          /**< PKCS#1 block type 0 padding*/
SCHEME_BLOCK_TYPE_1,          /**< PKCS#1 block type 1 padding*/
SCHEME_BLOCK_TYPE_2,          /**< PKCS#1 block type 2 padding*/
SCHEME_RSAES_OAEP_SHA1,       /**< PKCS#1 RSAES-OAEP-SHA1 padding*/
SCHEME_RSAES_OAEP_SHA224,     /**< PKCS#1 RSAES-OAEP-SHA224 padding*/
SCHEME_RSAES_OAEP_SHA256,     /**< PKCS#1 RSAES-OAEP-SHA256 padding*/
SCHEME_RSAES_OAEP_SHA384,     /**< PKCS#1 RSAES-OAEP-SHA384 padding*/
SCHEME_RSAES_OAEP_SHA512,     /**< PKCS#1 RSAES-OAEP-SHA512 padding*/
SCHEME_RSAES_PKCS1_V1_5,      /**< PKCS#1 RSAES-PKCS1_V1_5 padding*/
```

参考：

OAEP：Optimal asymmetric encryption padding（https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding）

>  https://blog.csdn.net/makenothing/article/details/88429511

## RSA和AES组合使用

RSA提供了重要的非对称加密，但速度慢；AES对称加密，简单快速。

常将RSA和AES组合使用，将AES在建立连接时通过RSA加密后发给通讯对方；同时RSA可以对数据进行签名防止被篡改。

## 密钥的读音问题

【mì yuè】读音下的“密钥”的意思：紧密的锁闭。这里的用法用了“密钥”的动词性质。
【 mì yào】读音下的“密钥”的意思：密码学中的专有名词，指解密所需要的特殊代码。这里用了“密钥”的名词性。
密钥现代用的最多的是密码学中的意思，在英文中解释为key，中文意思偏向于钥匙。在密码学中，特别是公钥密码体系中，密钥的形象描述往往是房屋或者保险箱的钥匙。因此在技术词典中，密钥被标注为【 mì yào】。
在一些词典中原来把密钥标注为【mì yuè】，由于权威性带来了一些影响，所以也有很多人把密钥念作【mì yuè】。由于钥在读作【 yuè 】也可以作“钥匙”的解释。但是钥被念作【 yuè 】时，往往偏向于钥的动词性，这种性质就跟“血”的用法相似。
总而言之，密钥一词虽然古来有之，但是密码学赋予了密钥一词新的含义，所以密钥的读法可以根据不同的背景来选择，可以读作【mì yào】，也可以读作【mì yuè】，但由于密码学的影响，现在人们普遍把密钥读作【mì yào】。