# forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Set up the queryset for parent_comment
    #     self.fields['parent_comment'].queryset = Comment.objects.all()
