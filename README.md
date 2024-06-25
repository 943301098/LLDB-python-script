# LLDB-python-script

接触IOS逆向没多长时间，记录自己的学习过程，在学习过程中自己写了一些非常简单的lldb脚本（或者整合一下常用的几个脚本），分享一下。。。



一、简化加载lldb步骤

USB动态调试时，debugserver步骤后，输入lldb,还要再手动输入

```process connect connect://127.0.0.1:8888```

进行连接，此处简化一下
仅需输入
```lldb```
之后按“c”即可，让lldb自动加载。




二、快速计算函数在ida中的偏移地址

![base64](https://user-images.githubusercontent.com/50468890/174735928-e9d735bc-cdb5-4033-b3a8-0cb3ae33522d.png)

