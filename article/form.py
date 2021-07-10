from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Article


class PostForm(forms.ModelForm):

    tag = forms.CharField(label='tag', widget=forms.TextInput(attrs={'placeholder': 'Enter tags separete by comma'}),
                          required=True,)

    class Meta:
        model = Article
        fields = ('author', 'title', 'content', 'published', 'tag')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'id_author', 'type': 'hidden'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'id': 'summernote', 'name': 'editordata'}),
            'tag': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'id_tag'}),
        }


class EditForm(forms.ModelForm):

    tag = forms.CharField(label='tag', widget=forms.TextInput(),
                          required=True,)

    class Meta:
        model = Article
        fields = ('title', 'content', 'published', 'tag')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'id': 'summernote', 'name': 'editordata'}),
            'tag': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'id_tag'}),
        }


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
