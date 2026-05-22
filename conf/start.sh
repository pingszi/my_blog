#!/bin/bash
nginx
uwsgi --ini /opt/project/product/script/uwsgi.ini
tail -f /opt/project/product/my_blog/logs/erablog.log