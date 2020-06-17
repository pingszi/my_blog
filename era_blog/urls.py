from django.conf.urls import url
from django.conf import settings
from django.urls import path, re_path, include
from django.conf.urls.static import static

from era_blog.views import Index, Friends, Detail, Archive, CategoryList, CategoryView, TagList, TagView, About, AllArticle


urlpatterns = [
    # 首页
    path('', Index.as_view(), name='index'),

    # 友情链接
    path('friends/', Friends.as_view(), name='friends'),

    # 文章详情
    re_path('article/av(?P<pk>\d+)', Detail.as_view(), name='detail'),

    # 文章归档
    path('article/', Archive.as_view(), name='archive'),

    # 分类统计
    path('category/', CategoryList.as_view(), name='category'),

    # 文章分类
    re_path('category/cg(?P<pk>\d+)', CategoryView.as_view(), name='article_category'),

    # 标签统计
    path('tag/', TagList.as_view(), name='tag'),

    # 文章标签
    re_path('tag/tg(?P<pk>\d+)', TagView.as_view(), name='article_tag'),

    # 关于本站
    path('about/', About.as_view(),name='about'),

    # 关于本站
    path('allArchive/', AllArticle.as_view(), name='allArchive'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)