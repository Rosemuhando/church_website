CONTENT_ADMIN_GROUP = 'Church Content Admin'


def is_content_admin(user):
    return bool(
        user.is_authenticated
        and user.is_active
        and user.groups.filter(name=CONTENT_ADMIN_GROUP).exists()
    )
