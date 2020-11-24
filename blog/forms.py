from django import forms
from .models import Feedback, Comment
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = "__all__"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author','text') 