from django.urls import path
from django.views.generic import RedirectView, TemplateView

from contact.views import contact_page, private_message
from sermons.views import sermon_list
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='About.html'), name='about'),
    path('announcements/', views.announcements, name='announcements'),
    path('sermons/', sermon_list, name='sermons'),
    path('events/', TemplateView.as_view(template_name='Events.html'), name='events'),
    path('contact/', contact_page, name='contact'),
    path('contact/message/', private_message, name='private_message'),
    path('gallery/', views.gallery, name='gallery'),
    path('teachings/', sermon_list, name='teachings'),
    path('ministry/', views.ministry, name='ministry'),
    path('giving/', TemplateView.as_view(template_name='Tith&Offerings.html'), name='giving'),
    path('tithes-offerings/', RedirectView.as_view(pattern_name='giving', permanent=False), name='tithes_offerings'),
]
