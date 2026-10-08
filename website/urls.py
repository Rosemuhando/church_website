from django.urls import path
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from contact.views import contact_page, private_message
from sermons.views import sermon_list
from . import views

urlpatterns = [
    path('login/', views.SiteLoginView.as_view(), name='login'),
    path('register/', views.SiteSignUpView.as_view(), name='register'),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.txt',
            subject_template_name='registration/password_reset_subject.txt',
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
    path('account/', views.user_dashboard, name='user_dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
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
