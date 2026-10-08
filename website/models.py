from django.db import models
from django.utils import timezone


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
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=500, blank=True)
    event_date = models.DateField(blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-uploaded_at']

    def __str__(self):
        return self.title
