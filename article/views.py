from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .form import CustomUserCreationForm, EditForm, PostForm, TagForm
from .models import Article, ArticleTag, Tag


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
        tag_list = ArticleTag.objects.filter(
            article_id=post.id).values_list('tag_id', flat=True)
        tag_name = []
        for tag in tag_list:
            tag_name.append(Tag.objects.get(id=tag))
        article_tags[post.id] = tag_name

    number_article = {}
    for tag in common_tags:
        number_article[tag.id] = ArticleTag.objects.filter(tag_id=tag).count()

    context = {
        'posts': posts,
        'common_tags': common_tags,
        'article_tags': article_tags.items(),
        'number_article': number_article.items(),
    }
    return render(request, 'article/home.html', context)


@login_required
def draftArticle(request):
    posts = Article.objects.filter(
        author=request.user, published=False).order_by('-created_date')

    common_tags = Tag.objects.all()

    article_tags = {}
    for post in posts:
        tag_list = ArticleTag.objects.filter(
            article_id=post.id).values_list('tag_id', flat=True)
        tag_name = []
        for tag in tag_list:
            tag_name.append(Tag.objects.get(id=tag))
        article_tags[post.id] = tag_name

    number_article = {}
    for tag in common_tags:
        number_article[tag.id] = ArticleTag.objects.filter(tag_id=tag).count()

    context = {
        'posts': posts,
        'common_tags': common_tags,
        'article_tags': article_tags.items(),
        'number_article': number_article.items(),
    }

    return render(request, 'article/draft_article.html', context)


def detailArticle(request, id):
    article = get_object_or_404(Article, id=id)
    common_tags = Tag.objects.all()
    tag_list = ArticleTag.objects.filter(
        article_id=article.id).values_list('tag_id', flat=True)
    article_tags = []
    for tag in tag_list:
        article_tags.append(Tag.objects.get(id=tag))

    context = {
        'article': article,
        'common_tags': common_tags,
        'article_tags': article_tags,
    }
    return render(request, 'article/article_detail.html', context)


@login_required
def addArticle(request):
    if request.method == "POST":
        article_form = PostForm(request.POST, prefix="article_form")
        tag_form = TagForm(request.POST, prefix="tag_form")
        if article_form.is_valid() and tag_form.is_valid():
            tag_list = tag_form.cleaned_data['tag'].split(',')
            for i in tag_list:
                if not Tag.objects.filter(name=i.strip()).exists():
                    Tag.objects.create(name=i.strip(), slug=i.strip())
            article_post = article_form.save()
            article_tag = tag_form.save(commit=False)
            article_tag.article_id = article_post
            article_tag.save()
            for i in tag_list:
                article_tag.tag_id.add(Tag.objects.get(name=i.strip()).id)
            article_tag.save()
        return redirect(viewArticle)
    else:
        article_form = PostForm(prefix="article_form")
        tag_form = TagForm(prefix="tag_form")
        context = {
            'article_form': article_form,
            'tag_form': tag_form,
        }

    return render(request, 'article/add_article.html', context)


@login_required
def editArticle(request, id):
    article_instance = get_object_or_404(Article, id=id)
    article_form = EditForm(request.POST or None,
                            instance=article_instance, prefix="article_form")

    tag_instance = get_object_or_404(
        ArticleTag, article_id=article_instance.id)
    tag_form = TagForm(
        request.POST or None, instance=tag_instance, prefix="tag_form")

    if article_form.is_valid() and tag_form.is_valid():
        tag_list = tag_form.cleaned_data['tag'].split(',')
        for i in tag_list:
            if not Tag.objects.filter(name=i.strip()).exists():
                Tag.objects.create(name=i.strip(), slug=i.strip())
        article_post = article_form.save()
        article_tag = ArticleTag.objects.get(article_id=article_post)
        new_tags = []
        for i in tag_list:
            new_tags.append(Tag.objects.get(name=i.strip()).id)
        article_tag.tag_id.set(new_tags)

        return redirect(viewArticle)

    context = {
        'article_form': article_form,
        'tag_form': tag_form,
        'article_instance': article_instance,
        'tag_instance': tag_instance
    }

    return render(request, 'article/update_article.html', context)


def tagged(request, id):
    common_tags = Tag.objects.all()
    tag = get_object_or_404(Tag, id=id)
    article_ids = ArticleTag.objects.filter(
        tag_id=tag).values_list('article_id', flat=True)

    posts = []
    for article_id in article_ids:
        posts.append(Article.objects.get(id=article_id))

    article_tags = {}
    for post in posts:
        tag_list = ArticleTag.objects.filter(
            article_id=post).values_list('tag_id', flat=True)
        tag_name = []
        for tag in tag_list:
            tag_name.append(Tag.objects.get(id=tag))
        article_tags[post.id] = tag_name

    number_article = {}
    for tag in common_tags:
        number_article[tag.id] = ArticleTag.objects.filter(tag_id=tag).count()

    context = {
        'tag': tag,
        'common_tags': common_tags,
        'number_article': number_article.items,
        'posts': posts,
        'article_tags': article_tags.items(),
    }
    return render(request, 'article/tags_article.html', context)
