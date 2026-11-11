from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core import mail
from django.core.exceptions import PermissionDenied
from django.test import TestCase, override_settings
from django.urls import reverse

from website.models import Announcement, PastorProfile, StaffAdminRequest
from website.permissions import CONTENT_ADMIN_GROUP, is_content_admin
from website.services import review_staff_admin_request


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

    def test_only_staff_can_open_admin(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.headers['Location'])

        member = get_user_model().objects.create_user(
            username='admin-page-member',
            password='Member-test-password-975!',
        )
        self.client.force_login(member)
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.headers['Location'])

        admin_user = get_user_model().objects.create_superuser(
            username='admin-page-superuser',
            email='admin-page@example.com',
            password='Admin-test-password-975!',
        )
        self.client.force_login(admin_user)
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

    def test_public_sign_in_page_does_not_advertise_admin_login(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Sign in to Admin')

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

    def test_member_sermon_page_does_not_advertise_admin_login(self):
        member = get_user_model().objects.create_user(
            username='sermon-page-member',
            password='Member-test-password-975!',
        )
        self.client.force_login(member)

        response = self.client.get(reverse('sermons'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Authorized staff sign in')

    def test_member_can_request_content_admin_access(self):
        member = get_user_model().objects.create_user(
            username='admin-applicant',
            password='Member-test-password-975!',
        )
        self.client.force_login(member)

        response = self.client.post(reverse('request_content_admin'))

        self.assertRedirects(response, reverse('user_dashboard'))
        admin_request = StaffAdminRequest.objects.get(user=member)
        self.assertEqual(admin_request.status, StaffAdminRequest.Status.PENDING)
        self.assertFalse(is_content_admin(member))

    def test_only_superuser_can_approve_content_admin_request(self):
        member = get_user_model().objects.create_user(
            username='admin-applicant',
            password='Member-test-password-975!',
        )
        admin_request = StaffAdminRequest.objects.create(user=member)
        ordinary_user = get_user_model().objects.create_user(
            username='ordinary-reviewer',
            password='Member-test-password-975!',
        )

        with self.assertRaises(PermissionDenied):
            review_staff_admin_request(admin_request, ordinary_user, approved=True)

        superuser = get_user_model().objects.create_superuser(
            username='request-approver',
            email='approver@example.com',
            password='Admin-test-password-975!',
        )
        review_staff_admin_request(admin_request, superuser, approved=True)
        member.refresh_from_db()
        admin_request.refresh_from_db()

        self.assertTrue(is_content_admin(member))
        self.assertFalse(member.is_staff)
        self.assertEqual(admin_request.status, StaffAdminRequest.Status.APPROVED)
        self.assertEqual(admin_request.reviewed_by, superuser)

        review_staff_admin_request(admin_request, superuser, approved=False)
        member.refresh_from_db()
        self.assertFalse(is_content_admin(member))
        self.assertEqual(admin_request.status, StaffAdminRequest.Status.REJECTED)

    def test_approved_content_admin_gets_separate_limited_panel(self):
        content_admin = get_user_model().objects.create_user(
            username='content-admin',
            password='Admin-test-password-975!',
        )
        content_admin.groups.add(
            Group.objects.create(name=CONTENT_ADMIN_GROUP),
        )
        self.client.force_login(content_admin)

        response = self.client.post(reverse('login'), {
            'username': content_admin.username,
            'password': 'Admin-test-password-975!',
        })
        self.assertRedirects(response, reverse('staff_panel'))

        panel = self.client.get(reverse('staff_panel'))
        self.assertEqual(panel.status_code, 200)
        self.assertContains(panel, 'Post an announcement')
        self.assertContains(panel, 'Add a pastor or update a pastor card')

        admin_page = self.client.get(reverse('admin:index'))
        self.assertEqual(admin_page.status_code, 302)
        self.assertIn('/admin/login/', admin_page.headers['Location'])

        response = self.client.post(reverse('staff_panel'), {
            'action': 'announcement',
            'title': 'Service update',
            'content': 'Sunday service begins at 9 AM.',
            'event_date': '',
        })
        self.assertRedirects(response, reverse('staff_panel'))
        self.assertTrue(Announcement.objects.filter(title='Service update').exists())

    def test_content_admin_can_add_and_edit_pastor_cards(self):
        content_admin = get_user_model().objects.create_user(
            username='pastor-card-admin',
            password='Admin-test-password-975!',
        )
        content_admin.groups.add(
            Group.objects.create(name=CONTENT_ADMIN_GROUP),
        )
        self.client.force_login(content_admin)

        response = self.client.post(reverse('staff_panel'), {
            'action': 'pastor-profile',
            'name': 'Pastor New',
            'title': 'Reverend',
            'biography': 'A church leader serving the community.',
            'display_order': '4',
        })
        self.assertRedirects(response, reverse('staff_panel'))
        profile = PastorProfile.objects.get(name='Pastor New')
        self.assertEqual(profile.slug, 'pastor-new')

        response = self.client.post(reverse('staff_panel'), {
            'action': 'pastor-profile',
            'profile_id': str(profile.pk),
            'name': 'Reverend New',
            'title': 'Reverend',
            'biography': 'Updated ministry description.',
            'display_order': '1',
        })
        self.assertRedirects(response, reverse('staff_panel'))
        profile.refresh_from_db()
        self.assertEqual(profile.name, 'Reverend New')
        self.assertEqual(profile.biography, 'Updated ministry description.')

    def test_staff_panel_has_mobile_friendly_photo_and_video_inputs(self):
        content_admin = get_user_model().objects.create_user(
            username='media-content-admin',
            password='Admin-test-password-975!',
        )
        content_admin.groups.add(
            Group.objects.create(name=CONTENT_ADMIN_GROUP),
        )
        self.client.force_login(content_admin)

        response = self.client.get(reverse('staff_panel'))

        self.assertContains(response, 'accept="image/*"')
        self.assertContains(response, 'accept="video/*"')

    def test_regular_member_cannot_open_content_admin_panel(self):
        member = get_user_model().objects.create_user(
            username='panel-member',
            password='Member-test-password-975!',
        )
        self.client.force_login(member)

        response = self.client.get(reverse('staff_panel'))

        self.assertEqual(response.status_code, 403)

    def test_about_page_shows_editable_pastor_profiles(self):
        response = self.client.get(reverse('about'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reverend Anthony')
        self.assertContains(response, 'Pastor Judy')
        self.assertContains(response, 'Pastor Michael')
        self.assertContains(response, 'serving the congregation with faith')

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

    @override_settings(MAILERS={
        'default': {
            'BACKEND': 'django.core.mail.backends.locmem.EmailBackend',
        },
    })
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

    def test_unapproved_staff_flag_does_not_grant_content_admin_access(self):
        staff_user = get_user_model().objects.create_user(
            username='administrator',
            password='test-password',
            is_staff=True,
        )

        response = self.client.post(reverse('login'), {
            'username': staff_user.username,
            'password': 'test-password',
        })

        self.assertRedirects(response, reverse('user_dashboard'))

    def test_superuser_signs_in_to_superadmin_site(self):
        superuser = get_user_model().objects.create_superuser(
            username='superadministrator',
            email='superadministrator@example.com',
            password='test-password',
        )

        response = self.client.post(reverse('login'), {
            'username': superuser.username,
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
