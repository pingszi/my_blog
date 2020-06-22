from datetime import datetime
from django.db import models
from django.utils.html import format_html
from mdeditor.fields import MDTextField


class Tag(models.Model):
    """
    文章标签
    """

    class Meta:
        # **表名
        db_table = "blog_tag"
        # **菜单名
        verbose_name = "文章标签"
        verbose_name_plural = "文章标签"

    def __str__(self):
        return str(self.name)

    id = models.AutoField(primary_key=True, verbose_name="编号")
    name = models.CharField(max_length=30, verbose_name='标签名称')
    enabled = models.BooleanField(default=True, verbose_name="启用")

    # 统计文章数 并放入后台
    def get_items(self):
        return self.article_set.all().count()
    get_items.short_description = '文章数'


class Category(models.Model):
    """
    文章分类
    """

    class Meta:
        # **表名
        db_table = "blog_category"
        # **菜单名
        verbose_name = "文章分类"
        verbose_name_plural = "文章分类"

    def __str__(self):
        return self.name

    id = models.AutoField(primary_key=True, verbose_name="编号")
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=99, verbose_name='分类排序')
    active = models.BooleanField(default=True, verbose_name='是否添加到菜单')
    icon = models.CharField(max_length=30, default='fa fa-home', verbose_name='菜单图标')

    # 统计文章数 并放入后台
    def get_items(self):
        return self.article_set.all().count()
    get_items.short_description = '文章数'

    def icon_data(self):
        return format_html(
            '<i class="{}"></i>',
            self.icon,
        )
    icon_data.short_description = '图标预览'


class Article(models.Model):
    """
    文章
    """

    class Meta:
        # **表名
        db_table = "blog_article"
        # **菜单名
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title

    id = models.AutoField(primary_key=True, verbose_name="编号")
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.TextField(max_length=100, verbose_name='文章描述')
    cover = models.ImageField(upload_to='article/%Y/%m/',verbose_name='文章封面')
    content = MDTextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='发布时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='文章分类', on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(Tag, verbose_name='文章标签')
    enabled = models.BooleanField(default=True, verbose_name="启用")

    def cover_data(self):
        return format_html(
            '<img src="{}" width="156px" height="98px"/>',
            self.cover.url,
        )
    cover_data.short_description = '文章封面'

    def viewed(self):
        """
        增加阅读数
        """
        self.click_count += 1
        self.save(update_fields=['click_count'])


class Links(models.Model):
    """
    友情链接
    """

    class Meta:
        # **表名
        db_table = "blog_links"
        # **菜单名
        verbose_name = '友链'
        verbose_name_plural = '友链'

    def __str__(self):
        return self.url

    id = models.AutoField(primary_key=True, verbose_name="编号")
    title = models.CharField(max_length=50, verbose_name='标题')
    url = models.URLField(verbose_name='地址')
    desc = models.TextField(verbose_name='描述', max_length=250)
    image = models.URLField(default='https://image.3001.net/images/20190330/1553875722169.jpg', verbose_name='头像')

    def avatar_data(self):
        return format_html(
            '<img src="{}" width="50px" height="50px" style="border-radius: 50%;" />',
            self.image,
        )
    avatar_data.short_description = '头像'

    def avatar_admin(self):
        return format_html(
            '<img src="{}" width="250px" height="250px"/>',
            self.image,
        )
    avatar_admin.short_description = '头像预览'
