from django.contrib import admin
from .models import *


class SectionInLine(admin.StackedInline):
    model = ArticleSection


class ArticlesAdmin(admin.ModelAdmin):
    inlines = [
        SectionInLine,
    ]

admin.site.register(Article, ArticlesAdmin)
admin.site.register(ArticleComponentText)
admin.site.register(ArticleComponentImage)
