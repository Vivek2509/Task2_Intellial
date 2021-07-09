from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .form import CustomUserCreationForm, EditForm, PostForm
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
            return redirect("login")
    else:
        article_tags = ArticleTag.objects.filter(article=article.id)

        context = {
            'article': article,
            'article_tags': article_tags,
        }

        return render(request, 'article/article_detail.html', context)


@login_required
def addArticle(request):
    if request.method == "POST":
        article_form = PostForm(request.POST)
        if article_form.is_valid():
            tag_list = article_form.cleaned_data['tag'].split(',')

            new_tags = []
            for tag in tag_list:
                if tag != ' ' and tag != '':
                    if not Tag.objects.filter(name=tag.strip()).exists():
                        new_tags.append(tag.strip())

            # Add tag in to Tag table
            tag_instances = [ArticleTag(name=tag, slug=tag)
                             for tag in new_tags]
            Tag.objects.bulk_create(tag_instances)

            article_post = article_form.save()

            # Create new ArticleTag instance
            article_tag_instances = [ArticleTag(
                article=article_post, tag=Tag.objects.get(name=tag)) for tag in new_tags]
            ArticleTag.objects.bulk_create(article_tag_instances)

        return redirect(viewArticle)
    else:
        article_form = PostForm()
        context = {
            'article_form': article_form,
        }

    return render(request, 'article/add_article.html', context)


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

        tag_instances = [ArticleTag(name=tag, slug=tag)
                         for tag in new_tags]
        Tag.objects.bulk_create(tag_instances)

        article_post = article_form.save()

        # Delete old ArticleTag instance
        ArticleTag.objects.filter(article=article_post).delete()

        # Add new ArticleTag instance
        article_tag_instances = [ArticleTag(
            article=article_post, tag=Tag.objects.get(name=tag)) for tag in new_tags]
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
    print(article_tags)

    tags_numbers = article_tags.values(
        'tag__name', 'tag__id').annotate(tag_count=Count('article'))

    context = {
        'tag': tag,
        'articles': articles,
        'article_tags': article_tags,
        'tags_numbers': tags_numbers
    }
    return render(request, 'article/tags_article.html', context)
