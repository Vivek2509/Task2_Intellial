from django.urls import path, include
from .views import viewArticle, addArticle, AddArticleView, UpdateArticleView, draftArticle, ArticleDetailView, register


urlpatterns = [
    path('',viewArticle),
    path('public/article', viewArticle, name="home"),
    path('public/article/<int:pk>', ArticleDetailView.as_view(), name="detail_article"),
    path('add_article',addArticle, name="add_article"),
    path('edit_article/<int:pk>',UpdateArticleView.as_view(), name="edit_article"),
    path('draft_article',draftArticle, name="draft_article"),
    #path('tag/<int:pk>/', tagged, name="tagged"),
    path("accounts/register/", register, name="register"),
]
