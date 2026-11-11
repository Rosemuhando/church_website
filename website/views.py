import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from sermons.forms import SermonForm
from sermons.models import Sermon

from .forms import (
    AnnouncementForm,
    GalleryPhotoForm,
    MemberCreationForm,
    PastorPhotoForm,
)
from .models import Announcement, GalleryPhoto, PastorProfile, StaffAdminRequest
from .permissions import is_content_admin


class SiteLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to
        if self.request.user.is_superuser:
            return reverse_lazy('admin:index')
        if is_content_admin(self.request.user):
            return reverse_lazy('staff_panel')
        return reverse_lazy('user_dashboard')


class SiteSignUpView(CreateView):
    form_class = MemberCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('user_dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('admin:index')
            if is_content_admin(request.user):
                return redirect('staff_panel')
            return redirect('user_dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


@login_required
def user_dashboard(request):
    if request.user.is_superuser:
        return redirect('admin:index')
    if is_content_admin(request.user):
        return redirect('staff_panel')
    admin_request = StaffAdminRequest.objects.filter(user=request.user).first()
    return render(request, 'account/dashboard.html', {
        'admin_request': admin_request,
    })


@login_required
def request_content_admin(request):
    if request.method != 'POST':
        return redirect('user_dashboard')
    if request.user.is_superuser or is_content_admin(request.user):
        return redirect('user_dashboard')

    admin_request, created = StaffAdminRequest.objects.get_or_create(
        user=request.user,
    )
    if not created and admin_request.status == StaffAdminRequest.Status.REJECTED:
        admin_request.status = StaffAdminRequest.Status.PENDING
        admin_request.reviewed_at = None
        admin_request.reviewed_by = None
        admin_request.save(
            update_fields=('status', 'reviewed_at', 'reviewed_by'),
        )
    messages.success(request, 'Your content admin request has been submitted.')
    return redirect('user_dashboard')


@login_required
def staff_panel(request):
    if request.user.is_superuser:
        return redirect('admin:index')
    if not is_content_admin(request.user):
        raise PermissionDenied

    forms = {
        'announcement': AnnouncementForm(),
        'photo': GalleryPhotoForm(),
        'teaching': SermonForm(),
        'pastor_photo': PastorPhotoForm(),
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'announcement':
            form = AnnouncementForm(request.POST)
        elif action == 'photo':
            form = GalleryPhotoForm(request.POST, request.FILES)
        elif action == 'teaching':
            form = SermonForm(request.POST, request.FILES)
        elif action == 'pastor-photo':
            profile = get_object_or_404(
                PastorProfile,
                pk=request.POST.get('profile_id'),
            )
            form = PastorPhotoForm(
                request.POST,
                request.FILES,
                instance=profile,
            )
            if not request.FILES.get('photo'):
                form.add_error('photo', 'Choose a photo to upload.')
        else:
            raise PermissionDenied('Unknown content action.')

        form_key = 'pastor_photo' if action == 'pastor-photo' else action
        if action in ('photo', 'teaching', 'pastor-photo'):
            if not os.environ.get('CLOUDINARY_URL'):
                messages.error(
                    request,
                    'Media uploads are not configured. Set CLOUDINARY_URL in Render first.',
                )
                forms[form_key] = form
            elif form.is_valid():
                form.save()
                messages.success(request, 'Your content was saved.')
                return redirect('staff_panel')
            else:
                forms[form_key] = form
        elif form.is_valid():
            form.save()
            messages.success(request, 'Your content was saved.')
            return redirect('staff_panel')
        else:
            forms[action] = form

    return render(request, 'website/staff_panel.html', {
        'announcement_form': forms['announcement'],
        'photo_form': forms['photo'],
        'teaching_form': forms['teaching'],
        'pastor_photo_form': forms['pastor_photo'],
        'pastor_profiles': PastorProfile.objects.all(),
        'recent_announcements': Announcement.objects.all()[:5],
        'recent_photos': GalleryPhoto.objects.all()[:5],
        'recent_teachings': Sermon.objects.all()[:5],
        'media_uploads_enabled': bool(os.environ.get('CLOUDINARY_URL')),
    })


def home(request):
    return render(request, 'website/home.html', {'page_title': 'Home'})


def about(request):
    return render(request, 'About.html', {
        'pastor_profiles': PastorProfile.objects.all(),
    })


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
