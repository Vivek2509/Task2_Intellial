from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Article, ArticleTag, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('author', 'title', 'content', 'published')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'id_author', 'type': 'hidden'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'id': 'summernote', 'name': 'editordata'}),
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content', 'published')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'id': 'summernote', 'name': 'editordata'}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ('tag',)

        widgets = {
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
