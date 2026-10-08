from django.contrib import admin

from .models import Announcement, GalleryPhoto


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'event_date', 'important')
    list_filter = ('important', 'date')
    search_fields = ('title', 'content')
    date_hierarchy = 'date'


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'display_order', 'is_published', 'uploaded_at')
    list_editable = ('display_order', 'is_published')
    list_filter = ('is_published', 'event_date')
    search_fields = ('title', 'caption')
    readonly_fields = ('uploaded_at',)
