from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .form import CustomUserCreationForm, EditForm
from .models import Article, ArticleTag, Tag
from django.http import HttpResponse


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
    articles = Article.objects.filter(published=True).order_by('-created_date')
    article_ids = [article.id for article in articles]

    article_tags = ArticleTag.objects.filter(article__in=article_ids)

    tags_numbers = article_tags.values(
        'tag__name', 'tag__id').annotate(tag_count=Count('article'))

    context = {
        'articles': articles,
        'article_tags': article_tags,
        'tags_numbers': tags_numbers,
    }
    return render(request, 'article/home.html', context)


@login_required
def draftArticle(request):
    articles = Article.objects.filter(
        author=request.user, published=False).order_by('-created_date')

    article_ids = [article.id for article in articles]

    article_tags = ArticleTag.objects.filter(article__in=article_ids)

    context = {
        'articles': articles,
        'article_tags': article_tags,
    }
    return render(request, 'article/draft_article.html', context)


def detailArticle(request, id):
    article = get_object_or_404(Article, id=id)
    if not article.published:
        if article.author == request.user:
            article_tags = ArticleTag.objects.filter(article=article.id)

            context = {
                'article': article,
                'article_tags': article_tags,
            }

            return render(request, 'article/article_detail.html', context)
        else:
            return redirect(viewArticle)
    else:
        article_tags = ArticleTag.objects.filter(article=article.id)

        context = {
            'article': article,
            'article_tags': article_tags,
        }

        return render(request, 'article/article_detail.html', context)


@login_required
def addArticle(request):
    if request.POST.get('action') == 'post':
        title = request.POST.get('title')
        content = request.POST.get('content')
        published = request.POST.get('published') == 'true'
        tag_list = request.POST.get('tag').split(',')

        article_instance = Article.objects.create(
            author=request.user,
            title=title,
            content=content,
            published=published
        )

        new_tags = []
        for tag in tag_list:
            if tag != ' ' and tag != '':
                if not Tag.objects.filter(name=tag.strip()).exists():
                    new_tags.append(tag.strip())

        # Add tag in to Tag table
        tag_instances = [Tag(name=tag, slug=tag)
                         for tag in new_tags]
        Tag.objects.bulk_create(tag_instances)

        new_tags = []
        for tag in tag_list:
            if tag != ' ' and tag != '':
                new_tags.append(tag.strip())

        # Create new ArticleTag instance
        article_tag_instances = [ArticleTag(
            article=article_instance, tag=Tag.objects.get(name=tag)) for tag in new_tags]
        ArticleTag.objects.bulk_create(article_tag_instances)

        return HttpResponse()
    else:
        return render(request, 'article/add_article.html')


@login_required
def editArticle(request, id):
    article_instance = get_object_or_404(Article, id=id)
    article_form = EditForm(request.POST or None, instance=article_instance)

    # For send data to form as instance
    article_tags = ArticleTag.objects.filter(
        article=article_instance.id).values_list('tag__name', flat=True)

    if article_form.is_valid():
        tag_list = article_form.cleaned_data['tag'].split(',')

        new_tags = []
        for tag in tag_list:
            if tag != ' ' and tag != '':
                if not Tag.objects.filter(name=tag.strip()).exists():
                    new_tags.append(tag.strip())

        tag_instances = [Tag(name=tag, slug=tag)
                         for tag in new_tags]
        Tag.objects.bulk_create(tag_instances)

        article_post = article_form.save()

        new_tags = []
        for tag in tag_list:
            if tag != ' ' and tag != '':
                new_tags.append(tag.strip())

        # Delete old ArticleTag instance
        delete_tags = list(set(article_tags) - set(new_tags))
        for tag in delete_tags:
            ArticleTag.objects.get(article=article_post,
                                   tag=Tag.objects.get(name=tag)).delete()

        # Add new ArticleTag instance
        add_tags = list(set(new_tags) - set(article_tags))
        article_tag_instances = [ArticleTag(
            article=article_post, tag=Tag.objects.get(name=tag)) for tag in add_tags]

        ArticleTag.objects.bulk_create(article_tag_instances)

        return redirect(viewArticle)

    context = {
        'article_form': article_form,
        'article_instance': article_instance,
        'article_tags': article_tags
    }

    return render(request, 'article/edit_article.html', context)


def tagged(request, id):
    tag = get_object_or_404(Tag, id=id)
    articles = ArticleTag.objects.filter(tag=tag)

    article_ids = [article.article.id for article in articles]

    article_tags = ArticleTag.objects.filter(article__in=article_ids)

    context = {
        'tag': tag,
        'articles': articles,
        'article_tags': article_tags,
    }
    return render(request, 'article/tags_article.html', context)
