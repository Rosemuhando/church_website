from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Announcement, GalleryPhoto, PastorProfile


class MemberCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'content', 'event_date', 'important')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }


class GalleryPhotoForm(forms.ModelForm):
    class Meta:
        model = GalleryPhoto
        fields = ('title', 'image', 'caption', 'event_date')
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }


class PastorPhotoForm(forms.ModelForm):
    class Meta:
        model = PastorProfile
        fields = ('photo',)
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
