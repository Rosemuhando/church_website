from django.db import models
from cloudinary.models import CloudinaryField


class Sermon(models.Model):
    title = models.CharField(max_length=200)
    preacher = models.CharField(max_length=120)
    date = models.DateField(blank=True, null=True)
    bible_verse = models.CharField(max_length=120, blank=True)
    content = models.TextField(blank=True)
    video = CloudinaryField('video', resource_type='video', blank=True, null=True)
    video_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return self.title
