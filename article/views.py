from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse
from .models import Article, Tag, ArticleTag
from .form import ArticleForm, CustomUserCreationForm, PostForm, EditForm


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
    ##common_tags = Article.tags.most_common()
    context = {
        'posts':posts,
        #'common_tags':common_tags,
    }
    return render(request, 'article/home.html', context)

@login_required
def draftArticle(request):
    posts = Article.objects.filter(published=False).order_by('-created_date');
    #common_tags = Article.tags.most_common()
    context = {
        'posts':posts,
        #'common_tags':common_tags,
    }
    return render(request, 'article/draft_article.html', context)

class AddArticleView(CreateView):
	model = Article
	form_class = PostForm
	template_name = 'article/add_article.html'

class ArticleDetailView(DetailView):
	model = Article
	template_name = 'article/article_detail.html'

class UpdateArticleView(UpdateView):
	model = Article
	form_class = EditForm
	template_name = 'article/update_article.html'

@login_required
def addArticle(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            tag_list = form.cleaned_data['tag'].split(',')
            for i in tag_list:
                if not Tag.objects.filter(name=i.strip()).exists():
                    Tag.objects.create(name=i.strip(),slug=i.strip())
            task = form.save()
            instance = ArticleTag.objects.create(article_id=task)
            for i in tag_list:
                instance.tag_id.add(list(Tag.objects.filter(name=i.strip()).values_list('id', flat=True))[0])
        return redirect(viewArticle)
    else:
        form = ArticleForm()
        context = {
            'form':form,
        }

    return render(request, 'article/add_article.html', context)

#list(ArticleTag.objects.filter(article_id=3).values_list('tag_id', flat=True))



# @login_required
# def editArticle(request, id):
#     instance = get_object_or_404(Article, id=id)
#     form = ArticleForm(request.POST or None, instance=instance)
#     if form.is_valid():
#         newpost = form.save(commit=False)
#         if  form.cleaned_data['published']:
#             newpost.publish()
#             newpost.save()
#             form.save_m2m()
#         else:
#             newpost.save()
#             form.save_m2m()
#         return redirect(viewArticle)
#     context = {
#             'form':form,
#         }
#     return render(request, 'article/add_article.html', context)

# def tagged(request, pk):
#     tag = get_object_or_404(Tag, id=pk)
#     common_tags = Article.tags.most_common()
#     posts = Article.objects.filter(tags=tag)
#     context = {
#         'tag':tag,
#         'common_tags':common_tags,
#         'posts':posts,
#     }
#     return render(request, 'article/home.html', context)
