# my_blog
## 我的个人博客
- 在[Django-Hexo-Matery](https://github.com/sqlsec/Django-Hexo-Matery)项目的基础上开发
- 基于python django框架的个人博客模版；

# 项目地址
- [my_blog](http://time.pings.fun)

# 安装
## 安装运行环境
pip install -r my_blog/docker/requirements.txt
## 正式环境部署
- 通过docker方式部署；
```
docker build -t pings/my_blog -f my_blog/docker/Dockerfile .
docker run -p 80:80 -p 8088:8088 -v /root/uploads/myblog:/opt/project/product/my_blog/uploads --name my_blog pings/my_blog
```

# 界面
## 首页
![首页](https://github.com/pingszi/my_blog/tree/master/era_blog/static/image/blog-1.png)
## 分类
![分类](https://github.com/pingszi/my_blog/tree/master/era_blog/static/image/blog-2.png)
## 文章
![文章](https://github.com/pingszi/my_blog/tree/master/era_blog/static/image/blog-3.png)
## 分类(移动端)
![分类(移动端)](https://github.com/pingszi/my_blog/tree/master/era_blog/static/image/blog-4.png)
## 文章(移动端)
![文章(移动端)](https://github.com/pingszi/my_blog/tree/master/era_blog/static/image/blog-5.png)
## 搜索(移动端)
![搜索(移动端)](https://github.com/pingszi/my_blog/tree/master/era_blog/static/image/blog-6.png)

# 更新记录
- 2020-06-17 项目开发完成
- 2020-06-19 完善