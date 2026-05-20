import os
import random
import datetime
import markdown
import json
import html as html_module

from django.shortcuts import render
from django.views.generic.base import View
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.storage import default_storage
from pure_pagination import Paginator, PageNotAnInteger

from .models import Links, Article, Category, Tag
from my_blog import settings


def global_setting(request):
    """
    将settings里面的变量 注册为全局变量
    """
    active_categories = Category.objects.filter(active=True, parent=None).order_by('index')
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DESC': settings.SITE_DESCRIPTION,
        'SITE_KEY': settings.SECRET_KEY,
        'SITE_MAIL': settings.SITE_MAIL,
        'SITE_ICP': settings.SITE_ICP,
        'SITE_ICP_URL': settings.SITE_ICP_URL,
        'SITE_TITLE': settings.SITE_TITLE,
        'SITE_TYPE_CHINESE': settings.SITE_TYPE_CHINESE,
        'SITE_TYPE_ENGLISH': settings.SITE_TYPE_ENGLISH,
        'active_categories': active_categories
    }


class Index(View):
    """
    首页展示
    """
    def get(self, request):
        all_articles = Article.objects.filter(enabled=True).defer('content').order_by('-add_time')
        top_articles = Article.objects.filter(enabled=True, is_recommend=1).defer('content').order_by('-add_time')
        # 首页分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_articles, 9, request=request)
        articles = p.page(page)

        return render(request, 'index.html', {
            'all_articles': articles,
            'top_articles': top_articles,
        })


class Friends(View):
    """
    友链链接展示
    """
    def get(self, request):
        links = Links.objects.all()
        card_num = random.randint(1, 10)
        return render(request, 'friends.html', {
            'links': links,
            'card_num': card_num,
        })


def mermaid_fence_format(source, language, class_name, options, md, **kwargs):
    """自定义 mermaid 代码块渲染为 script 标签，避免浏览器解析 < 破坏语法"""
    source = html_module.unescape(source)
    # 过滤 nl2br 等扩展可能插入的 <br> 标签
    source = source.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
    # 过滤 Windows 换行符和多余空白
    source = source.replace('\r', '').strip()
    # 使用 script 标签包裹，浏览器不会解析其中的 < > 字符
    return '<script type="text/mermaid">\n%s\n</script>' % source


class Detail(View):
    """
    文章详情页
    """
    def get(self, request, pk):
        article = Article.objects.get(id=int(pk))
        article.viewed()
        md = markdown.Markdown(
            extensions=[
                'nl2br',
                'pymdownx.highlight',
                'pymdownx.superfences',
                'pymdownx.tasklist',
                'pymdownx.tilde',
                'tables',
                'toc',
            ],
            extension_configs={
                'pymdownx.superfences': {
                    'custom_fences': [
                        {
                            'name': 'mermaid',
                            'class': 'mermaid',
                            'format': mermaid_fence_format,
                        }
                    ]
                }
            }
        )
        output = md.convert(article.content)

        #**查找上一篇
        previous_article = Article.objects.filter(enabled=True, category=article.category, id__lt=pk).defer('content').order_by('-id')[:1]
        previous_article = previous_article[0] if len(previous_article) else None
        #**查找下一篇
        next_article = Article.objects.filter(enabled=True, category=article.category, id__gt=pk).defer('content').order_by('id')[:1]
        next_article = next_article[0] if len(next_article) else None

        return render(request, 'detail.html', {
            'article': article,
            'previous_article': previous_article,
            'next_article': next_article,
            'detail_html': output,
        })


class Archive(View):
    """
    文章归档
    """
    def get(self, request):
        all_articles = Article.objects.filter(enabled=True).defer('content').order_by('-add_time')
        all_date = all_articles.values('add_time')
        latest_date = all_date[0]['add_time']
        all_date_list = []
        for i in all_date:
            all_date_list.append(i['add_time'].strftime("%Y-%m-%d"))

        # 遍历1年的日期
        end = datetime.date(latest_date.year, latest_date.month, latest_date.day)
        begin = datetime.date(latest_date.year-1, latest_date.month, latest_date.day)
        d = begin
        date_list = []
        temp_list = []

        delta = datetime.timedelta(days=1)
        while d <= end:
            day = d.strftime("%Y-%m-%d")
            if day in all_date_list:
                temp_list.append(day)
                temp_list.append(all_date_list.count(day))
            else:
                temp_list.append(day)
                temp_list.append(0)
            d += delta
            date_list.append(temp_list)
            temp_list = []

        # 文章归档分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_articles, 10, request=request)
        articles = p.page(page)

        return render(request, 'archive.html', {
            'all_articles': articles,
            'date_list': date_list,
            'end': str(end),
            'begin': str(begin),
        })


class CategoryList(View):
    def get(self, request):
        categories = Category.objects.filter(active=True, parent=None).order_by('index')

        return render(request, 'category.html', {
            'categories': categories,
        })


class CategoryView(View):
    def get(self, request, pk):
        categories = Category.objects.filter(active=True, parent=None).order_by('index')
        current_category = Category.objects.get(id=int(pk))
        # 如果是父分类，同时展示其子分类的文章
        category_ids = [current_category.id]
        if current_category.parent is None:
            child_ids = list(current_category.get_children().values_list('id', flat=True))
            category_ids.extend(child_ids)
        articles = Article.objects.filter(enabled=True, category_id__in=category_ids).defer('content').order_by('-add_time')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(articles, 9, request=request)
        articles = p.page(page)

        # 确定当前展开的父分类ID
        if current_category.parent is None:
            active_parent_id = current_category.id
        else:
            active_parent_id = current_category.parent_id

        return render(request, 'article_category.html', {
            'categories': categories,
            'pk': int(pk),
            'active_parent_id': active_parent_id,
            'articles': articles
        })


class TagList(View):
    def get(self, request):
        tags = Tag.objects.filter(enabled=True)
        return render(request, 'tag.html', {
            'tags': tags,
        })


class TagView(View):
    def get(self, request, pk):
        tags = Tag.objects.filter(enabled=True)
        articles = Tag.objects.get(id=int(pk)).article_set.filter(enabled=True).defer('content').order_by('-add_time')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(articles, 9, request=request)
        articles = p.page(page)

        return render(request, 'article_tag.html', {
            'tags': tags,
            'pk': int(pk),
            'articles': articles,
        })


class About(View):
    def get(self, request):
        articles = Article.objects.filter(enabled=True).defer('content').order_by('-add_time')
        categories = Category.objects.filter(active=True)
        tags = Tag.objects.filter(enabled=True)

        all_date = articles.values('add_time')

        latest_date = all_date[0]['add_time']
        end_year = latest_date.strftime("%Y")
        end_month = latest_date.strftime("%m")
        date_list = []
        for i in range(int(end_month), 13):
            date = str(int(end_year)-1)+'-'+str(i).zfill(2)
            date_list.append(date)

        for j in range(1, int(end_month)+1):
            date = end_year + '-' + str(j).zfill(2)
            date_list.append(date)

        value_list = []
        all_date_list = []
        for i in all_date:
            all_date_list.append(i['add_time'].strftime("%Y-%m"))

        for i in date_list:
            value_list.append(all_date_list.count(i))

        temp_list = []  # 临时集合
        tags_list = []  # 存放每个标签对应的文章数
        for tag in tags:
            temp_list.append(tag.name)
            temp_list.append(len(tag.article_set.filter(enabled=True)))
            tags_list.append(temp_list)
            temp_list = []

        tags_list.sort(key=lambda x: x[1], reverse=True)  # 根据文章数排序

        top10_tags = []
        top10_tags_values = []
        for i in tags_list[:10]:
            top10_tags.append(i[0])
            top10_tags_values.append(i[1])

        return render(request, 'about.html', {
            'articles': articles,
            'categories': categories,
            'tags': tags,
            'date_list': date_list,
            'value_list': value_list,
            'top10_tags': top10_tags,
            'top10_tags_values': top10_tags_values
        })


class AllArticle(View):
    def get(self, request):
        articles = Article.objects.filter(enabled=True).order_by('-add_time').values('id', 'title', 'desc')
        rst = [{'id': d['id'], 'title': d['title'], 'content': d['desc']} for d in articles]
        return HttpResponse(json.dumps(rst, ensure_ascii=False))


class MartorUploadView(View):
    """
    Martor上传图片到默认存储（七牛云）
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(MartorUploadView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        upload_image = request.FILES.get("markdown-image-upload", None)

        if not upload_image:
            return JsonResponse({'status': 400, 'error': '未获取到要上传的图片'})

        # 格式检查
        ext = os.path.splitext(upload_image.name)[1].lower()
        if ext not in {'.jpg', '.jpeg', '.png', '.gif'}:
            return JsonResponse({'status': 400, 'error': '上传图片格式错误，只允许 jpg/png/gif'})

        # 保存到默认存储（七牛云）
        file_path = 'editor/{0:%Y%m%d%H%M%S%f}{1}'.format(datetime.datetime.now(), ext)
        file_url = default_storage.save(file_path, upload_image)
        full_url = os.path.join(settings.MEDIA_URL, file_url)

        return JsonResponse({
            'status': 200,
            'name': upload_image.name,
            'link': full_url
        })