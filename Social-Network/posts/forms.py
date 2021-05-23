from django import forms
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'shareInput','placeholder': " What's on your mind..." }))
    image = forms.ImageField( label='   :@', widget=forms.FileInput(attrs={'class':'imageShare'}))
    class Meta:
        model = Post
        fields = ('content', 'image')

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', 
                            widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))
    class Meta:
        model = Comment
        fields = ('body',)