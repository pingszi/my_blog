#!/bin/bash
nginx
uwsgi --ini /opt/project/product/script/uwsgi.ini
tail -f /var/log/nginx/error.log