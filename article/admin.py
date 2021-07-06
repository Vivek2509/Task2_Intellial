from django.contrib import admin
from .models import Article, Tag, ArticleTag

admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(ArticleTag)
