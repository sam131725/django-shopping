from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for creating/editing posts"""
    class Meta:
        model = Post
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'block w-full px-4 py-3 rounded-lg bg-accent/20 border border-accent/40 focus:border-transparent focus:ring-2 focus:ring-primary transition-all cursor-pointer',
                'accept': 'image/*',
            }),
            'caption': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 rounded-lg bg-accent/20 border border-accent/40 focus:border-transparent focus:ring-2 focus:ring-primary transition-all',
                'placeholder': 'Write a caption for your outfit...',
                'rows': 4,
                'maxlength': 500,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = 'Upload Photo'
        self.fields['caption'].label = 'Caption (Optional)'


class CommentForm(forms.ModelForm):
    """Form for adding comments"""
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-accent/20 border border-accent/40 focus:border-transparent focus:ring-2 focus:ring-primary transition-all text-sm',
                'placeholder': 'Add a comment...',
                'maxlength': 300,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = ''
