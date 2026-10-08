from django.db import models


class PrivateMessage(models.Model):
    MESSAGE_TYPES = [
        ('prayer', 'Prayer Request'),
        ('inquiry', 'General Inquiry'),
        ('spiritual', 'Spiritual Support'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    message = models.TextField()
    confidential = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'private message'
        verbose_name_plural = 'private messages'

    def __str__(self):
        return f'{self.get_message_type_display()} from {self.name}'
