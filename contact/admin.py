from django.contrib import admin

from .models import PrivateMessage


@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'message_type', 'phone', 'created_at')
    list_filter = ('message_type', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('created_at',)
