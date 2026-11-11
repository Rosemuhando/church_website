
from django.contrib import admin
from django.core.exceptions import PermissionDenied

from .models import Announcement, GalleryPhoto, PastorProfile, StaffAdminRequest
from .services import review_staff_admin_request


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'event_date', 'important')
    list_filter = ('important', 'date')
    search_fields = ('title', 'content')
    date_hierarchy = 'date'


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'event_date',
        'display_order',
        'is_published',
        'uploaded_at',
    )
    list_editable = ('display_order', 'is_published')
    list_filter = ('is_published', 'event_date')
    search_fields = ('title', 'caption')
    readonly_fields = ('uploaded_at',)


@admin.register(PastorProfile)
class PastorProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'slug', 'display_order')
    list_editable = ('display_order',)
    search_fields = ('name', 'title', 'biography')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(StaffAdminRequest)
class StaffAdminRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'requested_at', 'reviewed_at', 'reviewed_by')
    list_filter = ('status',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user', 'requested_at', 'reviewed_at', 'reviewed_by')
    actions = ('approve_requests', 'reject_requests')

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_superuser

    def approve_requests(self, request, queryset):
        if not request.user.is_active or not request.user.is_superuser:
            raise PermissionDenied
        for admin_request in queryset:
            review_staff_admin_request(admin_request, request.user, approved=True)
        self.message_user(request, 'Selected content admin requests were approved.')
    approve_requests.short_description = 'Approve selected content admin requests'

    def reject_requests(self, request, queryset):
        if not request.user.is_active or not request.user.is_superuser:
            raise PermissionDenied
        for admin_request in queryset:
            review_staff_admin_request(admin_request, request.user, approved=False)
        self.message_user(request, 'Selected content admin requests were rejected.')
    reject_requests.short_description = 'Reject selected content admin requests'
