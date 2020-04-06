# kokoro-bot
公主连接会战机器人-可可萝

### 项目概述
本项目是以 OICQ(QQ) 协议驱动的高性能机器人开发框架 [Mirai](https://github.com/mamoe/mirai) 的 Python 接口库 [kuriyama](https://github.com/NatriumLab/python-mirai) 的基础上开发的.

### 搭建环境和使用
1.下载安装 [JDK8](https://www.oracle.com/java/technologies/javase-jdk8-downloads.html)  
2.下载最新的 [mirai-console](https://github.com/mamoe/mirai-console/releases)  
3.下载最新的 [mirai-api-http](https://github.com/mamoe/mirai-api-http/releases) 将其放入与 `mirai-console` 的同级目录 `plugins` 下.  
4.启动mirai客户端
``` bash
java -jar mirai-console.jar
```
5.安装 [python3](https://www.python.org/downloads/)  
6.安装`kuriyama`库
``` bash
pip install kuriyama
```
7.下载或者拉取源码, 执行`bot.py`即可


### 加入开发
本项目欢迎一切形式上的贡献(包括但不限于 `Issues`, `Pull Requests`, `Good Idea` 等)  
希望能有更多优秀的开发者加入到对项目的贡献上来.  

你的 `Star` 是最大的支持和鼓励.  

若你在使用的过程中遇到了问题, 欢迎[提出聪明的问题](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/master/README-zh_CN.md), 希望有人能让这个项目变得更好.  



### 鸣谢
感谢 [`mamoe`](https://github.com/mamoe) 提供 [`mirai`](https://github.com/mamoe/mirai) 这么一个如此精彩的项目.  
感谢 [`NatriumLab`](https://github.com/NatriumLab) 提供的 [`kuriyama`](https://github.com/NatriumLab/python-mirai) 即mirai-python接口库.  

### 许可证
使用 [`GNU AGPLv3`](https://choosealicense.com/licenses/agpl-3.0/) 作为本项目的开源许可证, 而由于原项目 [`mirai`](https://github.com/mamoe/mirai) 同样使用了 `GNU AGPLv3` 作为开源许可证, 因此你在使用时需要遵守相应的规则.  