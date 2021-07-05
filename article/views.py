from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .form import ArticleForm
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse
from .form import CustomUserCreationForm


def register(request):
    if request.method == "GET":
        return render(request, "registration/register.html", {"form": CustomUserCreationForm})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("home"))


def viewArticle(request):
    posts = Article.objects.filter(published=True).order_by('-created_date');
    common_tags = Article.tags.most_common()
    context = {
        'posts':posts,
        'common_tags':common_tags,
    }
    return render(request, 'article/home.html', context)

def detailArticle(request, id):
    post = get_object_or_404(Article, id=id)
    context = {
        'post':post,
    }
    return render(request, 'article/article_detail.html', context)

@login_required
def draftArticle(request):
    posts = Article.objects.filter(published=False).order_by('-created_date');
    common_tags = Article.tags.most_common()
    context = {
        'posts':posts,
        'common_tags':common_tags,
    }
    return render(request, 'article/draft_article.html', context)

@login_required
def addArticle(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            newpost = form.save(commit=False)
            if  form.cleaned_data['published']:
                newpost.publish()
                newpost.save()
                form.save_m2m()
            else:
                newpost.save()
                form.save_m2m()
        return redirect(viewArticle)
    else:
        form = ArticleForm()
        context = {
            'form':form,
        }

    return render(request, 'article/add_article.html', context)

@login_required
def editArticle(request, id):
    instance = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, instance=instance)
    if form.is_valid():
        newpost = form.save(commit=False)
        if  form.cleaned_data['published']:
            newpost.publish()
            newpost.save()
            form.save_m2m()
        else:
            newpost.save()
            form.save_m2m()

        return redirect(viewArticle)
    context = {
            'form':form,
        }
    return render(request, 'article/add_article.html', context)

def tagged(request, id):
    tag = get_object_or_404(Tag, id=id)
    common_tags = Article.tags.most_common()[:4]
    posts = Article.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'common_tags':common_tags,
        'posts':posts,
    }
    return render(request, 'article/home.html', context)
