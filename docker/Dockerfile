FROM python:3.7.7

#**维护者
MAINTAINER Pings 275598139@qq.com

#**环境变量
ENV LANG en_US.UTF-8
#**设置时区
RUN ln -s -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

WORKDIR /opt/project/product
COPY requirements.txt .
RUN pip install -r requirements.txt

# nginx
# 安装
RUN apt-get update
RUN apt -y install nginx
# 配置
WORKDIR /etc/nginx/conf.d
COPY conf/nginx/myblog.conf myblog.conf
# 替换nginx.conf
COPY conf/nginx/nginx.conf /etc/nginx/nginx.conf
RUN rm -f default.conf

# uwsgi
RUN pip3 install uwsgi
WORKDIR /opt/project/product/script
COPY conf/uwsgi/uwsgi.ini uwsgi.ini

# 启动脚本
COPY conf/start.sh /opt/project/product/start.sh

# 添加项目
WORKDIR /opt/project/product
RUN apt -y install git
RUN git clone -b qiniu-cloud https://github.com/pingszi/my_blog.git

# 正式模式配置settings
WORKDIR /opt/project/product/my_blog/my_blog
RUN sed -i "s/^DEBUG = True/DEBUG = False/" settings.py
# 修改七牛配置
RUN echo "QINIU_ACCESS_KEY = 'test'" >> settings.py
RUN echo "QINIU_SECRET_KEY = 'test'" >> settings.py

# 提取静态文件
RUN python3 /opt/project/product/my_blog/manage.py collectstatic

# 启动
WORKDIR /opt/project/product
CMD bash start.sh

# docker build -t pings/my_blog -f my_blog/docker/Dockerfile .
# docker run -p 80:80 -p 8088:8088 --name my_blog pings/my_blog