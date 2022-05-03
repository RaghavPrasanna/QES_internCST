from .models import Comment
from django import forms

# This is used for answering the questions
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control' }),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }