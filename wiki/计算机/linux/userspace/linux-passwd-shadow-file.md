

# Linux中的/etc/passwd和/etc/shadow文件

> refer: [Understanding the /etc/shadow File](https://linuxize.com/post/etc-shadow-file/)

```
mark:$6$.n.:17736:0:99999:7:::
[--] [----] [---] - [---] ----
|      |      |   |   |   |||+-----------> 9. Unused
|      |      |   |   |   ||+------------> 8. Expiration date
|      |      |   |   |   |+-------------> 7. Inactivity period
|      |      |   |   |   +--------------> 6. Warning period
|      |      |   |   +------------------> 5. Maximum password age
|      |      |   +----------------------> 4. Minimum password age
|      |      +--------------------------> 3. Last password change
|      +---------------------------------> 2. Encrypted Password
+----------------------------------------> 1. Username
```

1. Username. The string you type when you log into the system. The user account that exist on the system.

2. Encrypted Password. The password is using the `$type$salt$hashed` format. `$type` is the method cryptographic hash algorithm and can have the following values:

   - `$1$` – MD5
   - `$2a$` – Blowfish
   - `$2y$` – Eksblowfish
   - `$5$` – SHA-256
   - `$6$` – SHA-512

   If the password field contains an asterisk (`*`) or exclamation point (`!`), the user will not be able to login to the system using password authentication. Other login methods like [key-based authentication](https://linuxize.com/post/how-to-setup-passwordless-ssh-login/) or [switching to the user](https://linuxize.com/post/su-command-in-linux/) are still allowed.

   In older Linux systems, the user’s encrypted password was stored in the `/etc/passwd` file.

3. Last password change. This is the date when the password was last changed. The umber of days is counted since January 1, 1970 (epoch date).

4. Minimum password age. The number of days that must pass before the user password can be changed. Typically it is set to zero, which means that there is no minimum password age.

5. Maximum password age. The number of days after the user password must be changed. By default, this number is set to `99999`.

6. Warning period. The number of days before the password expires during which the user is warned that the password must be changed.

7. Inactivity period. The number of days after the user password expires before the user account is disabled. Typically this field is empty.

8. Expiration date. The date when the account was disabled. It is represented as an epoch date.

9. Unused. This field is ignored. It is reserved for future use.



## Linux中手动增加用户

此例增加一个名为api的用户，密码为api，不允许shell登入。

1. 改`/etc/passwd`:

```
api:x:501:501:api:/home:/bin/false
```

2. 用`openssl passwd -1`命令生成经过MD5加密的密码，写到`/etc/shadow`中：

```
api:$1$JowD9ZBr$Oiy0iY4nlj.JCGkM2gBCj1:10933:0:99999:7:::
```





