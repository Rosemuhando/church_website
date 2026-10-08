from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import Announcement, GalleryPhoto
from .forms import MemberCreationForm


class SiteLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to
        if self.request.user.is_staff:
            return reverse_lazy('admin:index')
        return reverse_lazy('user_dashboard')


class SiteSignUpView(CreateView):
    form_class = MemberCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('user_dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin:index')
            return redirect('user_dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


@login_required
def user_dashboard(request):
    if request.user.is_staff:
        return redirect('admin:index')
    return render(request, 'account/dashboard.html')


def home(request):
    return render(request, 'website/home.html', {'page_title': 'Home'})


def about(request):
    return render(request, 'website/about.html', {'page_title': 'About'})


@login_required
@login_required
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


@login_required
@login_required
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
