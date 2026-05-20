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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            field = super().formfield_for_foreignkey(db_field, request, **kwargs)
            # 构建树形选项列表
            choices = [('', '---------')]
            parents = Category.objects.filter(active=True, parent=None).order_by('index')
            for parent in parents:
                choices.append((parent.id, parent.name))
                children = parent.get_children()
                for child in children:
                    choices.append((child.id, f'\u00A0\u00A0\u00A0\u00A0└─ {child.name}'))
            field.choices = choices
            return field
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        css = {
            'all': ('css/admin-article.css',)
        }


# 分类
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'index', 'active', 'get_items', 'icon', 'icon_data')
    list_filter = ('parent', 'active')
    search_fields = ('name', )
    list_editable = ('active', 'index', 'icon', 'parent')


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

