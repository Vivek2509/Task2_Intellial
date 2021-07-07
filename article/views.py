from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse
from .models import Article, Tag, ArticleTag
from .form import CustomUserCreationForm, PostForm, EditForm
from django.db.models import Count


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
    posts = Article.objects.filter(published=True).order_by('-created_date')

    common_tags = Tag.objects.all()

    article_tags = {}
    for post in posts:
        article_tags[post.id] = post.tag.split(',')

    number_article = {}
    for tag in common_tags:
        number_article[tag.id] = len(ArticleTag.objects.filter(tag_id=tag))

    context = {
        'posts': posts,
        'common_tags': common_tags,
        'article_tags': article_tags.items(),
        'number_article': number_article.items(),
    }
    return render(request, 'article/home.html', context)

@login_required
def draftArticle(request):
    posts = Article.objects.filter(published=False).order_by('-created_date');

    common_tags = Tag.objects.all()

    article_tags = {}
    for post in posts:
        article_tags[post.id] = post.tag.split(',')

    number_article = {}
    for tag in common_tags:
        number_article[tag.id] = len(ArticleTag.objects.filter(tag_id=tag))

    context = {
        'posts': posts,
        'common_tags': common_tags,
        'article_tags': article_tags.items(),
        'number_article': number_article.items(),
    }

    return render(request, 'article/draft_article.html', context)


def detailArticle(request,id):
    article = get_object_or_404(Article, id=id)
    common_tags = Tag.objects.all()
    article_tags = article.tag.split(',')

    context = {
        'article': article,
        'common_tags': common_tags,
        'article_tags': article_tags,
    }
    return render(request, 'article/article_detail.html', context)


@login_required
def addArticle(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            tag_list = form.cleaned_data['tag'].split(',')
            for i in tag_list:
                if not Tag.objects.filter(name=i.strip()).exists():
                    Tag.objects.create(name=i.strip(),slug=i.strip())
            task = form.save()
            instance = ArticleTag.objects.create(article_id=task)
            for i in tag_list:
                instance.tag_id.add(Tag.objects.get(name=i.strip()).id)
        return redirect(viewArticle)
    else:
        form = PostForm()
        context = {
            'form':form,
        }

    return render(request, 'article/add_article.html', context)


@login_required
def editArticle(request, id):
    instance = get_object_or_404(Article, id=id)
    form = EditForm(request.POST or None, instance=instance)
    if form.is_valid():
        tag_list = form.cleaned_data['tag'].split(',')
        for i in tag_list:
            if not Tag.objects.filter(name=i.strip()).exists():
                Tag.objects.create(name=i.strip(),slug=i.strip())
        task = form.save()

        article = ArticleTag.objects.get(article_id=task)
        new_tags = []
        for i in tag_list:
            new_tags.append(Tag.objects.get(name=i.strip()).id)
        article.tag_id.set(new_tags)

        return redirect(viewArticle)

    context = {
        'form':form,
        'instance':instance
    }

    return render(request, 'article/update_article.html', context)


def tagged(request, id):
    common_tags = Tag.objects.all()
    tag = get_object_or_404(Tag, id=id)
    article_ids = ArticleTag.objects.filter(tag_id=tag)

    posts = []
    for article_id in article_ids:
        posts.append(Article.objects.filter(id=article_id.id))

    article_tags = {}
    for post in posts:
        article_tags[post[0].id] = post[0].tag.split(',')

    number_article = {}
    for tag in common_tags:
        number_article[tag.id] = len(ArticleTag.objects.filter(tag_id=tag))


    context = {
        'tag': tag,
        'common_tags': common_tags,
        'number_article': number_article.items,
        'posts': posts,
        'article_tags': article_tags.items(),
    }
    return render(request, 'article/tags_article.html', context)
