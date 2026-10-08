from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from .models import Sermon


class SermonAccessTests(TestCase):
    def test_public_can_view_sermons_without_add_form(self):
        response = self.client.get(reverse('sermons'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'name="title"')

    def test_anonymous_user_cannot_post_a_sermon(self):
        response = self.client.post(reverse('sermons'), {
            'title': 'Unauthorized sermon',
            'preacher': 'Visitor',
        })

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Sermon.objects.count(), 0)

    def test_staff_without_add_permission_cannot_post(self):
        user = get_user_model().objects.create_user(
            username='staff-without-permission',
            password='test-password',
            is_staff=True,
        )
        self.client.force_login(user)

        response = self.client.post(reverse('sermons'), {
            'title': 'Unauthorized sermon',
            'preacher': 'Staff member',
        })

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Sermon.objects.count(), 0)

    def test_staff_with_add_permission_can_submit(self):
        user = get_user_model().objects.create_user(
            username='sermon-editor',
            password='test-password',
            is_staff=True,
        )
        permission = Permission.objects.get(
            content_type__app_label='sermons',
            codename='add_sermon',
        )
        user.user_permissions.add(permission)
        self.client.force_login(user)

        response = self.client.post(reverse('sermons'), {
            'title': 'Walking in Faith',
            'preacher': 'Pastor Antony',
            'bible_verse': 'Hebrews 11:1',
            'content': 'Trust God in every season.',
        })

        self.assertRedirects(response, reverse('sermons'))
        self.assertTrue(Sermon.objects.filter(title='Walking in Faith').exists())
