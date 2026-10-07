from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('announcements/', views.announcements, name='announcements'),
    path('sermons/', views.sermons, name='sermons'),
    path('events/', views.events, name='events'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('teachings/', views.teachings, name='teachings'),
    path('ministry/', views.ministry, name='ministry'),
    path('tithes-offerings/', views.tithes_offerings, name='tithes_offerings'),
]
