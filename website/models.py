from django.db import models
from django.conf import settings
from django.utils import timezone
from cloudinary.models import CloudinaryField


class StaffAdminRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_admin_request',
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='reviewed_staff_admin_requests',
    )

    class Meta:
        ordering = ['status', 'requested_at']
        verbose_name = 'content admin request'
        verbose_name_plural = 'content admin requests'

    def __str__(self):
        return f'{self.user} - {self.get_status_display()}'


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField(default=timezone.localdate)
    event_date = models.DateField(blank=True, null=True)
    important = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return self.title


class GalleryPhoto(models.Model):
    title = models.CharField(max_length=160)
    image = CloudinaryField('image')
    caption = models.CharField(max_length=500, blank=True)
    event_date = models.DateField(blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-uploaded_at']

    def __str__(self):
        return self.title


class PastorProfile(models.Model):
    slug = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=160)
    title = models.CharField(max_length=80)
    biography = models.TextField()
    photo = CloudinaryField('image', blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.name
