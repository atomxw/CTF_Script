# FIX_PNG

**关于项目：**

- 一部分是来自于铜匠师傅的代码
- 目前分为2种方式，如果crc32出错，就会遍历宽高爆破crc32相同的宽高；另一种情况是如果crc32相同会自动尝试铜匠师傅的代码（根据IDAT层的数据暴力爆破宽高）

<br>

# 效果:

**正常情况：**

<img src="./images/image1.png">

**暴力爆破：**

<img src="./images/image2.png">