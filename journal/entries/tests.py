"""API auth tests.

The most important guarantee in this app: a user can only ever see and change
their own journal entries. Everything else here supports that.
"""
from datetime import date, datetime, timedelta, timezone as dt_timezone
from unittest import mock

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import JournalEntry

PASSWORD = 'Sup3r-secret-pw'


def make_user(email):
    return User.objects.create_user(username=email, email=email, password=PASSWORD)


class RegistrationTests(APITestCase):
    url = '/api/auth/registration/'

    def register(self, **overrides):
        data = {'email': 'new@example.com', 'password1': PASSWORD, 'password2': PASSWORD}
        data.update(overrides)
        return self.client.post(self.url, data, format='json')

    def test_register_creates_user_and_logs_them_in(self):
        response = self.register()

        self.assertIn(response.status_code, (status.HTTP_201_CREATED, status.HTTP_204_NO_CONTENT))
        self.assertTrue(User.objects.filter(email='new@example.com').exists())
        self.assertEqual(self.client.get('/api/auth/user/').status_code, status.HTTP_200_OK)

    def test_duplicate_email_rejected(self):
        """Regression: an unverified existing email used to allow a second account."""
        make_user('new@example.com')

        response = self.register()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(email__iexact='new@example.com').count(), 1)
        self.assertEqual(self.client.get('/api/auth/user/').status_code, status.HTTP_403_FORBIDDEN)

    def test_duplicate_email_rejected_case_insensitive(self):
        make_user('new@example.com')

        response = self.register(email='NEW@Example.com')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(email__iexact='new@example.com').count(), 1)

    def test_duplicate_of_api_registered_user_rejected(self):
        self.register()
        self.client.post('/api/auth/logout/')

        response = self.register(password1='An0ther-pw-here', password2='An0ther-pw-here')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(email__iexact='new@example.com').count(), 1)

    def test_mismatched_passwords_rejected(self):
        response = self.register(password2='something-else-entirely')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.exists())

    def test_weak_password_rejected(self):
        response = self.register(password1='password', password2='password')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.exists())


class LoginLogoutTests(APITestCase):
    def setUp(self):
        self.user = make_user('kia@example.com')

    def login(self, email='kia@example.com', password=PASSWORD):
        return self.client.post(
            '/api/auth/login/', {'email': email, 'password': password}, format='json'
        )

    def test_login_with_correct_credentials(self):
        response = self.login()

        self.assertIn(response.status_code, (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT))
        user_response = self.client.get('/api/auth/user/')
        self.assertEqual(user_response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_response.data['email'], 'kia@example.com')

    def test_login_with_wrong_password(self):
        response = self.login(password='wrong-password')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.client.get('/api/auth/user/').status_code, status.HTTP_403_FORBIDDEN)

    def test_login_with_unknown_email(self):
        response = self.login(email='nobody@example.com')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_ends_session(self):
        self.login()

        self.client.post('/api/auth/logout/')

        self.assertEqual(self.client.get('/api/auth/user/').status_code, status.HTTP_403_FORBIDDEN)


class UnauthenticatedAccessTests(APITestCase):
    def setUp(self):
        self.entry = JournalEntry.objects.create(user=make_user('a@example.com'), date=date(2026, 1, 1))

    def test_all_entry_endpoints_require_login(self):
        detail = f'/api/entries/{self.entry.pk}/'
        requests = [
            ('get', '/api/auth/user/'),
            ('get', '/api/entries/'),
            ('post', '/api/entries/'),
            ('get', '/api/entries/today/'),
            ('get', '/api/entries/recent/'),
            ('get', '/api/entries/by-date/2026-01-01/'),
            ('get', '/api/entries/range/'),
            ('get', detail),
            ('patch', detail),
            ('delete', detail),
        ]
        for method, url in requests:
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url, {}, format='json')
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertTrue(JournalEntry.objects.filter(pk=self.entry.pk).exists())


class EntryIsolationTests(APITestCase):
    """One user must never be able to read or modify another user's entries."""

    def setUp(self):
        self.alice = make_user('alice@example.com')
        self.bob = make_user('bob@example.com')
        self.alice_entry = JournalEntry.objects.create(
            user=self.alice, date=date(2026, 1, 1), log='Alice private thoughts'
        )
        self.bob_entry = JournalEntry.objects.create(
            user=self.bob, date=date(2026, 1, 1), log='Bob private thoughts'
        )
        self.client.force_authenticate(self.alice)

    def test_list_only_shows_own_entries(self):
        for url in ('/api/entries/', '/api/entries/recent/'):
            with self.subTest(url=url):
                response = self.client.get(url)
                ids = [e['id'] for e in response.data]
                self.assertEqual(ids, [self.alice_entry.pk])

    def test_cannot_read_another_users_entry(self):
        response = self.client.get(f'/api/entries/{self.bob_entry.pk}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_update_another_users_entry(self):
        response = self.client.patch(
            f'/api/entries/{self.bob_entry.pk}/', {'log': 'hacked'}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.bob_entry.refresh_from_db()
        self.assertEqual(self.bob_entry.log, 'Bob private thoughts')

    def test_cannot_delete_another_users_entry(self):
        response = self.client.delete(f'/api/entries/{self.bob_entry.pk}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(JournalEntry.objects.filter(pk=self.bob_entry.pk).exists())

    def test_by_date_returns_own_entry_not_another_users(self):
        response = self.client.get('/api/entries/by-date/2026-01-01/')

        self.assertEqual(response.data['id'], self.alice_entry.pk)
        self.assertEqual(response.data['log'], 'Alice private thoughts')

    def test_created_entry_belongs_to_requester_even_if_user_is_sent(self):
        response = self.client.post(
            '/api/entries/', {'date': '2026-02-01', 'user': self.bob.pk}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JournalEntry.objects.get(pk=response.data['id']).user, self.alice)

    def test_responses_do_not_expose_user_field(self):
        response = self.client.get(f'/api/entries/{self.alice_entry.pk}/')

        self.assertNotIn('user', response.data)


class EntryRangeTests(APITestCase):
    url = '/api/entries/range/'

    def setUp(self):
        self.alice = make_user('alice@example.com')
        self.bob = make_user('bob@example.com')
        for day, mood in [(1, 2), (5, 4), (10, 5)]:
            JournalEntry.objects.create(user=self.alice, date=date(2026, 3, day), mood=mood)
        JournalEntry.objects.create(user=self.bob, date=date(2026, 3, 5), mood=1)
        self.client.force_authenticate(self.alice)

    def test_returns_own_entries_in_range_oldest_first(self):
        response = self.client.get(self.url, {'start': '2026-03-01', 'end': '2026-03-07'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['start'], '2026-03-01')
        self.assertEqual(response.data['end'], '2026-03-07')
        self.assertEqual(
            [(e['date'], e['mood']) for e in response.data['entries']],
            [('2026-03-01', 2), ('2026-03-05', 4)],
        )

    def test_range_is_inclusive_and_includes_every_scale(self):
        response = self.client.get(self.url, {'start': '2026-03-10', 'end': '2026-03-10'})

        entry = response.data['entries'][0]
        self.assertEqual(entry['date'], '2026-03-10')
        for field in ('mood', 'anxiety_level', 'overall_day_rating', 'environment_quality'):
            self.assertIn(field, entry)
        self.assertNotIn('log', entry)

    def test_defaults_to_last_30_days(self):
        today = timezone.localdate()
        JournalEntry.objects.create(user=self.alice, date=today)
        JournalEntry.objects.create(user=self.alice, date=today - timedelta(days=29))
        JournalEntry.objects.create(user=self.alice, date=today - timedelta(days=30))

        response = self.client.get(self.url)

        self.assertEqual(response.data['end'], today.isoformat())
        self.assertEqual(response.data['start'], (today - timedelta(days=29)).isoformat())
        self.assertEqual(len(response.data['entries']), 2)

    def test_does_not_create_entries(self):
        self.client.get(self.url, {'start': '2026-04-01', 'end': '2026-04-30'})

        self.assertFalse(JournalEntry.objects.filter(date__month=4).exists())

    def test_invalid_ranges_rejected(self):
        cases = [
            {'start': 'not-a-date', 'end': '2026-03-07'},
            {'start': '2026-03-07', 'end': '2026-03-01'},
            {'start': '2025-01-01', 'end': '2026-03-01'},
        ]
        for params in cases:
            with self.subTest(params=params):
                response = self.client.get(self.url, params)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TodayTests(APITestCase):
    def test_today_uses_new_zealand_date_not_utc(self):
        """Regression: 9am in NZ is still the previous day in UTC."""
        self.client.force_authenticate(make_user('kia@example.com'))
        nine_am_nzdt = datetime(2026, 11, 21, 20, 0, tzinfo=dt_timezone.utc)  # 22 Nov 09:00 NZDT

        with mock.patch('django.utils.timezone.now', return_value=nine_am_nzdt):
            response = self.client.get('/api/entries/today/')

        self.assertEqual(response.data['date'], '2026-11-22')


class CsrfTests(APITestCase):
    """Session auth must reject state-changing requests without a CSRF token."""

    def setUp(self):
        self.user = make_user('kia@example.com')
        self.csrf_client = APIClient(enforce_csrf_checks=True)
        self.csrf_client.login(username='kia@example.com', password=PASSWORD)

    def test_post_without_csrf_token_rejected(self):
        response = self.csrf_client.post('/api/entries/', {'date': '2026-03-01'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(JournalEntry.objects.exists())

    def test_post_with_csrf_token_accepted(self):
        self.csrf_client.get('/app/')  # spa_view sets the csrftoken cookie
        token = self.csrf_client.cookies['csrftoken'].value

        response = self.csrf_client.post(
            '/api/entries/', {'date': '2026-03-01'}, format='json', HTTP_X_CSRFTOKEN=token
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SpaViewTests(APITestCase):
    def test_spa_routes_do_not_redirect_logged_out_users(self):
        """Regression: @login_required used to bounce /app/login to the API."""
        for url in ('/app/', '/app/login', '/app/register'):
            with self.subTest(url=url):
                response = self.client.get(url)
                # 200 when the frontend is built, 503 when it isn't; never a redirect
                self.assertIn(response.status_code, (200, 503))
