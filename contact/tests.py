from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import PrivateMessage


class PrivateMessageTests(TestCase):
    def test_contact_page_renders(self):
        response = self.client.get(reverse('contact'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact & Prayer')

    def test_valid_private_message_is_stored(self):
        response = self.client.post(reverse('private_message'), {
            'name': 'A Church Member',
            'phone': '0712345678',
            'email': 'member@example.com',
            'message_type': 'prayer',
            'message': 'Please pray for my family.',
            'confidential': 'on',
        })

        self.assertRedirects(response, f"{reverse('contact')}#private-message")
        self.assertEqual(PrivateMessage.objects.count(), 1)
        self.assertTrue(PrivateMessage.objects.get().confidential)

    def test_missing_privacy_consent_does_not_save(self):
        response = self.client.post(reverse('private_message'), {
            'name': 'A Church Member',
            'phone': '0712345678',
            'message_type': 'prayer',
            'message': 'Please pray for my family.',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PrivateMessage.objects.count(), 0)

    def test_private_messages_are_only_visible_in_admin(self):
        self.client.logout()
        response = self.client.get('/admin/contact/privatemessage/')
        self.assertEqual(response.status_code, 302)

        user = get_user_model().objects.create_user(
            username='not-staff',
            password='test-password',
        )
        self.client.force_login(user)
        response = self.client.get('/admin/contact/privatemessage/')
        self.assertEqual(response.status_code, 302)
