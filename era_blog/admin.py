from django.contrib import admin
from django.forms import TextInput, Textarea, SelectMultiple
from django.db import models

from .models import Links, Article, Category, Tag


admin.site.site_header="Pings博客后台"
admin.site.site_title="Pings博客"
admin.site.index_title="Pings博客"


# 文章
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'enabled', 'cover_data', 'is_recommend', 'add_time', 'update_time')
    search_fields = ('title', 'desc', 'content')
    list_filter = ('category', 'tag', 'add_time', 'enabled')
    list_editable = ('category', 'is_recommend', 'enabled')
    list_per_page = 20

    fieldsets = (
        ('编辑文章', {
            'classes': ('wide',),
            'fields': ('title', 'content')
        }),
        ('其他设置', {
            'fields': (('desc', 'tag', 'cover'), ('enabled', 'is_recommend', 'category')),
        }),
    )

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '59'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 59})},
        models.ManyToManyField: {'widget': SelectMultiple(attrs={'size': 3})},
    }

    class Media:
        css = {
            'all': ('css/admin-article.css',)
        }


# 分类
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index', 'active', 'get_items', 'icon', 'icon_data')
    search_fields = ('name', )
    list_editable = ('active', 'index', 'icon')


# 标签
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'enabled', 'get_items')
    search_fields = ('name', )
    list_filter = ('enabled', )
    list_editable = ('enabled', )
    list_per_page = 20


# 友链
@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url', 'avatar_data', 'desc')
    search_fields = ('title', 'url', 'desc')
    readonly_fields = ('avatar_admin', )
    list_editable = ('url',)

    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'desc', 'avatar_admin', 'image', )
        }),
    )

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '59'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 59})},
    }

