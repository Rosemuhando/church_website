from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse


class SiteAuthenticationTests(TestCase):
    def test_admin_can_open_gallery_photo_upload_form(self):
        admin_user = get_user_model().objects.create_superuser(
            username='gallery-admin',
            email='gallery-admin@example.com',
            password='Admin-test-password-975!',
        )
        self.client.force_login(admin_user)

        response = self.client.get(reverse('admin:website_galleryphoto_add'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="image"')

    def test_regular_member_cannot_manage_gallery_photos(self):
        member = get_user_model().objects.create_user(
            username='gallery-member',
            password='Member-test-password-975!',
        )
        self.client.force_login(member)

        response = self.client.get(reverse('admin:website_galleryphoto_add'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.headers['Location'])

    def test_member_pages_require_sign_in_and_return_to_requested_page(self):
        page_names = ('gallery', 'teachings', 'sermons', 'announcements')

        for page_name in page_names:
            with self.subTest(page=page_name):
                target = reverse(page_name)
                response = self.client.get(target)
                login_url = f"{reverse('login')}?next={target}"

                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.headers['Location'], login_url)
                login_page = self.client.get(login_url)
                self.assertContains(login_page, 'Please sign in as a church member')

    def test_sign_in_returns_member_to_requested_page(self):
        user = get_user_model().objects.create_user(
            username='member',
            password='test-password',
        )

        response = self.client.post(
            f"{reverse('login')}?next={reverse('gallery')}",
            {'username': user.username, 'password': 'test-password'},
        )

        self.assertRedirects(response, reverse('gallery'))

    def test_admin_sign_in_shortcut_uses_shared_login(self):
        response = self.client.get(reverse('backend_login'))

        self.assertRedirects(response, reverse('login'))

    def test_registration_creates_regular_user_and_starts_session(self):
        response = self.client.post(reverse('register'), {
            'username': 'new-member',
            'email': 'member@example.com',
            'password1': 'Safe-test-password-975!',
            'password2': 'Safe-test-password-975!',
        })

        user = get_user_model().objects.get(username='new-member')
        self.assertRedirects(response, reverse('user_dashboard'))
        self.assertTrue(self.client.session.get('_auth_user_id'))
        self.assertEqual(user.email, 'member@example.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_registration_rejects_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'new-member',
            'email': 'member@example.com',
            'password1': 'Safe-test-password-975!',
            'password2': 'Different-password-123!',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.filter(username='new-member').exists())

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_password_reset_email_changes_the_password(self):
        user = get_user_model().objects.create_user(
            username='member',
            email='member@example.com',
            password='Original-test-password-985!',
        )

        response = self.client.post(reverse('password_reset'), {
            'email': user.email,
        })

        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        reset_url = next(
            line for line in mail.outbox[0].body.splitlines()
            if line.startswith('http://')
        )
        reset_path = reset_url.removeprefix('http://testserver')
        reset_page = self.client.get(reset_path, follow=True)
        self.assertContains(reset_page, 'Set new password')

        response = self.client.post(reset_page.request['PATH_INFO'], {
            'new_password1': 'New-safe-password-986!',
            'new_password2': 'New-safe-password-986!',
        })

        self.assertRedirects(response, reverse('password_reset_complete'))
        user.refresh_from_db()
        self.assertTrue(user.check_password('New-safe-password-986!'))

    def test_regular_user_signs_in_to_account(self):
        user = get_user_model().objects.create_user(
            username='member',
            password='test-password',
        )

        response = self.client.post(reverse('login'), {
            'username': user.username,
            'password': 'test-password',
        })

        self.assertRedirects(response, reverse('user_dashboard'))
        self.assertEqual(self.client.session['_auth_user_id'], str(user.pk))

    def test_staff_user_signs_in_to_admin(self):
        staff_user = get_user_model().objects.create_user(
            username='administrator',
            password='test-password',
            is_staff=True,
        )

        response = self.client.post(reverse('login'), {
            'username': staff_user.username,
            'password': 'test-password',
        })

        self.assertRedirects(response, reverse('admin:index'))

    def test_account_requires_sign_in(self):
        response = self.client.get(reverse('user_dashboard'))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('user_dashboard')}",
        )

    def test_sign_out_clears_session(self):
        user = get_user_model().objects.create_user(
            username='member',
            password='test-password',
        )
        self.client.force_login(user)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)
