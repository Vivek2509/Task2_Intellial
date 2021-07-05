from django.urls import path, include
from .views import viewArticle, addArticle, editArticle, draftArticle, detailArticle, tagged,  register


urlpatterns = [
    path('public/article', viewArticle, name="home"),
    path('public/article/<int:id>/', detailArticle, name="detail_article"),
    path('add_article',addArticle, name="add_article"),
    path('edit_article/<int:id>/',editArticle, name="edit_article"),
    path('draft_article',draftArticle, name="draft_article"),
    path('tag/<int:id>/', tagged, name="tagged"),
    path("accounts/register/", register, name="register"),
]
