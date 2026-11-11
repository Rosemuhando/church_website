from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify

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


class PastorProfileForm(forms.ModelForm):
    class Meta:
        model = PastorProfile
        fields = ('name', 'title', 'biography', 'photo', 'display_order')
        widgets = {
            'biography': forms.Textarea(attrs={'rows': 4}),
            'photo': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        if not profile.slug:
            base_slug = slugify(profile.name) or 'pastor'
            profile.slug = base_slug
            suffix = 2
            while PastorProfile.objects.filter(slug=profile.slug).exclude(
                pk=profile.pk,
            ).exists():
                profile.slug = f'{base_slug}-{suffix}'
                suffix += 1
        if commit:
            profile.save()
            self.save_m2m()
        return profile
