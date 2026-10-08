from django import forms

from .models import Sermon


class SermonForm(forms.ModelForm):
    class Meta:
        model = Sermon
        fields = ['title', 'preacher', 'date', 'bible_verse', 'content', 'video', 'video_url']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter sermon title'}),
            'preacher': forms.TextInput(attrs={'placeholder': "Enter preacher's name"}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'bible_verse': forms.TextInput(attrs={'placeholder': 'Example: John 3:16'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write the sermon here...'}),
            'video': forms.FileInput(attrs={'accept': 'video/*'}),
            'video_url': forms.URLInput(attrs={'placeholder': 'YouTube or other video link'}),
        }
