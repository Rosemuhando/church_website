from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from .models import StaffAdminRequest
from .permissions import CONTENT_ADMIN_GROUP


def review_staff_admin_request(admin_request, reviewer, approved):
    if not reviewer.is_active or not reviewer.is_superuser:
        raise PermissionDenied('Only an active superuser can review admin requests.')

    if approved:
        if (
            not admin_request.user.is_active
            or admin_request.user.is_staff
            or admin_request.user.is_superuser
        ):
            raise PermissionDenied(
                'Only active member accounts can become content admins.'
            )
        group, _ = Group.objects.get_or_create(name=CONTENT_ADMIN_GROUP)
        admin_request.user.groups.add(group)
    else:
        group = Group.objects.filter(name=CONTENT_ADMIN_GROUP).first()
        if group:
            admin_request.user.groups.remove(group)

    admin_request.status = (
        StaffAdminRequest.Status.APPROVED
        if approved
        else StaffAdminRequest.Status.REJECTED
    )
    admin_request.reviewed_by = reviewer
    admin_request.reviewed_at = timezone.now()
    admin_request.save(update_fields=('status', 'reviewed_by', 'reviewed_at'))
