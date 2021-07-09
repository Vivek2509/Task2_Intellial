from django.urls import path

from .views import (addArticle, detailArticle, draftArticle, editArticle,
                    register, tagged, viewArticle)

urlpatterns = [
    path('', viewArticle, name="home"),
    # path('public/article', viewArticle, name="home"),
    path('article/<int:id>/', detailArticle, name="detail_article"),
    path('article/<int:id>/edit_article/', editArticle, name="edit_article"),
    path('article/add_article/', addArticle, name="add_article"),
    path('article/draft_article/', draftArticle, name="draft_article"),
    path('tag/<int:id>/', tagged, name="tagged"),
    path("accounts/register/", register, name="register"),
]
