import logging

from django.apps import AppConfig


class EraBlogConfig(AppConfig):
    name = 'era_blog'

    # **app名称
    verbose_name = "Pings博客后台"

logger = logging.getLogger("erablog")
