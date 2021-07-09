from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.article) + " | " + str(self.tag)
