from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']