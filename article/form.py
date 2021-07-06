from django import forms
from .models import Article, Tag, ArticleTag
from django.contrib.auth.forms import UserCreationForm

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['publish_date']

class PostForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ('title', 'author', 'content','tag' , 'published')

		widgets = {
			'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'id_author','type':'hidden'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
			'content': forms.Textarea(attrs={'class': 'form-control','id':'summernote','name':'editordata'}),
			'tag': forms.TextInput(attrs={'class': 'form-control'}),
		}


class EditForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ('title','content', 'tag' , 'published')

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'content': forms.Textarea(attrs={'class': 'form-control','id':'summernote','name':'editordata'}),
			'tag': forms.TextInput(attrs={'class': 'form-control'}),
		}


class TagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
