from django.shortcuts import render

from .models import Announcement, GalleryPhoto


def home(request):
    return render(request, 'website/home.html', {'page_title': 'Home'})


def about(request):
    return render(request, 'website/about.html', {'page_title': 'About'})


def announcements(request):
    return render(request, 'Announcement.htm', {
        'announcements': Announcement.objects.all(),
    })


def sermons(request):
    return render(request, 'website/sermons.html', {'page_title': 'Sermons'})


def events(request):
    return render(request, 'website/events.html', {'page_title': 'Events'})


def contact(request):
    return render(request, 'website/contact.html', {'page_title': 'Contact'})


def gallery(request):
    return render(request, 'Gallery.html', {
        'photos': GalleryPhoto.objects.filter(is_published=True),
    })


def teachings(request):
    return render(request, 'website/teachings.html', {'page_title': 'Teachings'})


def ministry(request):
    return render(request, 'website/ministry.html', {'page_title': 'Ministry'})


def tithes_offerings(request):
    return render(request, 'website/tithes_offerings.html', {'page_title': 'Tithes & Offerings'})
