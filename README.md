# Ycollect收藏夹

## 简介

这是一个使用flask框架和少量html,css,js编写的收藏夹程序，基于开源项目[webstatck](https://github.com/WebStackPage/WebStackPage.github.io)进行精简化页面。

如需使用成品，请按照以下方法使用：

- 没有python：点击 [这里](https://www.123pan.com/s/eFnlVv-6UVrh.html) 直接到达网盘下载，下载后解压文件到任意文件夹双击运行即可
- 有python环境：直接下载本项目源码后安装必要的库文件，之后双击运行main.py即可

## 文件说明

1. **data.json**:存放收藏的网站的数据文件
2. **port.txt**:flask项目运行的端口位置（为了防止端口冲突）
3. **main.py**:flask入口文件
4. **web.spec**:使用pyinstaller生成的一个spec配置文件
5. **static**文件夹：存放静态文件
6. **templates文件夹**：存放flask模板文件

## TODO

1. 实现记忆网站密码功能，防止忘记密码
2. [success]修改分类名称（当前认为不太需要）