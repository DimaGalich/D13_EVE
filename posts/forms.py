from django import forms

from .models import Reply, Post



class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label='Содержимое')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
