from django.urls import path

from .views import (add_article, detail_article, draft_article, edit_article,
                    register, tagged, view_article)

urlpatterns = [
    path('', view_article, name="home"),
    # path('public/article', viewArticle, name="home"),
    path('article/<int:id>/', detail_article, name="detail_article"),
    path('article/<int:id>/edit_article/', edit_article, name="edit_article"),
    path('article/add_article/', add_article, name="add_article"),
    path('article/draft_article/', draft_article, name="draft_article"),
    path('tag/<int:id>/', tagged, name="tagged"),
    path("accounts/register/", register, name="register"),
]
