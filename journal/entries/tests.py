"""API auth tests.

The most important guarantee in this app: a user can only ever see and change
their own journal entries. Everything else here supports that.
"""
import csv
import io
import json
import re
from datetime import date, datetime, timedelta, timezone as dt_timezone
from unittest import mock

from django.contrib.auth.models import User
from django.core import mail
from django.core.cache import cache
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


class EntryValuesTests(APITestCase):
    def setUp(self):
        self.client.force_authenticate(make_user('kia@example.com'))

    def test_spiritual_connection_saves_and_reads_back(self):
        created = self.client.post('/api/entries/', {'date': '2026-03-01', 'spiritual_connection': 4}, format='json')

        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.get(f"/api/entries/{created.data['id']}/").data['spiritual_connection'], 4)
        scales = self.client.get('/api/entries/range/', {'start': '2026-03-01', 'end': '2026-03-01'})
        self.assertEqual(scales.data['entries'][0]['spiritual_connection'], 4)

    def test_sliders_must_be_1_to_5(self):
        for value in (0, 6, 99):
            with self.subTest(value=value):
                response = self.client.post('/api/entries/', {'date': '2026-03-02', 'mood': value}, format='json')

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn('mood', response.data)

    def test_sliders_accept_1_to_5_and_blank(self):
        response = self.client.post('/api/entries/', {
            'date': '2026-03-03', 'mood': 1, 'stress_level': 5, 'spiritual_connection': None,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


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


class LegacyTemplatesRemovedTests(APITestCase):
    def test_root_redirects_to_spa(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/app/')

    def test_old_template_routes_are_gone(self):
        for url in ('/entries/', '/entries/new/', '/entries/1/', '/summary/', '/login/', '/logout/'):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_admin_view_on_site_points_at_spa(self):
        entry = JournalEntry.objects.create(user=make_user('a@example.com'), date=date(2026, 1, 1))

        self.assertEqual(entry.get_absolute_url(), f'/app/entries/{entry.pk}')


class PasswordResetTests(APITestCase):
    request_url = '/api/auth/password/reset/'
    confirm_url = '/api/auth/password/reset/confirm/'
    link_pattern = re.compile(r'http://testserver/app/reset-password/(?P<uid>[^/\s]+)/(?P<token>[^/\s]+)')

    def setUp(self):
        cache.clear()  # throttle counts live in the cache
        self.user = make_user('kia@example.com')

    def request_reset(self, email='kia@example.com'):
        return self.client.post(self.request_url, {'email': email}, format='json')

    def reset_link(self):
        match = self.link_pattern.search(mail.outbox[-1].body)
        self.assertIsNotNone(match, mail.outbox[-1].body)
        return match['uid'], match['token']

    def confirm(self, uid, token, password='Brand-new-pw-42'):
        return self.client.post(self.confirm_url, {
            'uid': uid, 'token': token, 'new_password1': password, 'new_password2': password,
        }, format='json')

    def test_sends_email_with_link_to_the_spa(self):
        response = self.request_reset()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, ['kia@example.com'])
        self.assertEqual(email.subject, 'Reset your Hauora Journal password')
        self.assertNotIn('example.com!', email.body)  # allauth's default "Hello from example.com!"
        self.reset_link()

    def test_unknown_email_gets_same_response_and_no_email(self):
        """Don't reveal which emails have accounts."""
        response = self.request_reset('nobody@example.com')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0)

    def test_link_sets_new_password(self):
        self.request_reset()
        uid, token = self.reset_link()

        response = self.confirm(uid, token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Brand-new-pw-42'))
        self.assertFalse(self.user.check_password(PASSWORD))

    def test_link_only_works_once(self):
        self.request_reset()
        uid, token = self.reset_link()
        self.confirm(uid, token)

        response = self.confirm(uid, token, password='Another-new-pw-77')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Brand-new-pw-42'))

    def test_bad_token_rejected(self):
        self.request_reset()
        uid, _ = self.reset_link()

        response = self.confirm(uid, 'not-a-real-token')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(PASSWORD))

    def test_weak_new_password_rejected(self):
        self.request_reset()
        uid, token = self.reset_link()

        response = self.confirm(uid, token, password='password')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_requests_are_rate_limited(self):
        for _ in range(5):
            self.assertEqual(self.request_reset().status_code, status.HTTP_200_OK)

        self.assertEqual(self.request_reset().status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(len(mail.outbox), 5)

    def test_signup_sends_no_email(self):
        """Verification is off until the app has a confirm-email page."""
        self.client.post('/api/auth/registration/', {
            'email': 'new@example.com', 'password1': PASSWORD, 'password2': PASSWORD,
        }, format='json')

        self.assertEqual(len(mail.outbox), 0)


class AccountExportTests(APITestCase):
    url = '/api/account/export/'

    def setUp(self):
        self.user = make_user('kia@example.com')
        JournalEntry.objects.create(
            user=self.user, date=date(2026, 3, 2), mood=4,
            log='Haere mai, whānau.\nSecond line, with "quotes"',
        )
        JournalEntry.objects.create(user=self.user, date=date(2026, 3, 1), mood=2)
        JournalEntry.objects.create(user=make_user('other@example.com'), date=date(2026, 3, 1), log='not yours')
        self.client.force_authenticate(self.user)

    def test_requires_login(self):
        self.client.force_authenticate(None)

        self.assertEqual(self.client.get(self.url).status_code, status.HTTP_403_FORBIDDEN)

    def test_json_contains_account_and_only_own_entries_oldest_first(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('attachment; filename="hauora-journal-', response['Content-Disposition'])
        self.assertTrue(response['Content-Disposition'].endswith('.json"'))
        self.assertEqual(response['Cache-Control'], 'no-store')
        data = json.loads(response.content)
        self.assertEqual(data['account']['email'], 'kia@example.com')
        self.assertEqual([e['date'] for e in data['entries']], ['2026-03-01', '2026-03-02'])
        self.assertEqual(data['entries'][1]['log'], 'Haere mai, whānau.\nSecond line, with "quotes"')
        self.assertNotIn('not yours', response.content.decode())

    def test_csv_has_one_row_per_entry_and_survives_newlines(self):
        response = self.client.get(self.url, {'file': 'csv'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response['Content-Type'].startswith('text/csv'))
        text = response.content.decode('utf-8')
        self.assertTrue(text.startswith('﻿'), 'BOM so Excel shows macrons')
        rows = list(csv.DictReader(io.StringIO(text.lstrip('﻿'))))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['date'], '2026-03-01')
        self.assertEqual(rows[1]['log'], 'Haere mai, whānau.\nSecond line, with "quotes"')
        self.assertNotIn('id', rows[0])

    def test_unknown_format_rejected(self):
        self.assertEqual(self.client.get(self.url, {'file': 'xml'}).status_code, status.HTTP_400_BAD_REQUEST)


class AccountDeleteTests(APITestCase):
    url = '/api/account/delete/'

    def setUp(self):
        cache.clear()  # throttle counts live in the cache
        self.user = make_user('kia@example.com')
        JournalEntry.objects.create(user=self.user, date=date(2026, 3, 1), log='mine')
        self.other = make_user('other@example.com')
        JournalEntry.objects.create(user=self.other, date=date(2026, 3, 1), log='theirs')
        self.client.login(username='kia@example.com', password=PASSWORD)

    def delete_account(self, password=PASSWORD):
        return self.client.post(self.url, {'password': password}, format='json')

    def test_deletes_user_and_their_entries_only(self):
        response = self.delete_account()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email='kia@example.com').exists())
        self.assertEqual(list(JournalEntry.objects.values_list('log', flat=True)), ['theirs'])
        self.assertTrue(User.objects.filter(pk=self.other.pk).exists())

    def test_session_is_logged_out(self):
        self.delete_account()

        self.assertEqual(self.client.get('/api/auth/user/').status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_or_missing_password_keeps_account(self):
        for password in ('wrong-password', ''):
            with self.subTest(password=password):
                response = self.delete_account(password)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn('password', response.json())
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())
        self.assertEqual(JournalEntry.objects.count(), 2)

    def test_requires_login(self):
        self.client.logout()

        self.assertEqual(self.delete_account().status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_requires_csrf_token(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        csrf_client.login(username='kia@example.com', password=PASSWORD)

        response = csrf_client.post(self.url, {'password': PASSWORD}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_password_guessing_is_throttled(self):
        for _ in range(5):
            self.delete_account('wrong-password')

        self.assertEqual(self.delete_account().status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())


class PrivacyPageTests(APITestCase):
    def test_privacy_and_account_pages_are_spa_routes(self):
        for url in ('/app/privacy', '/app/account'):
            with self.subTest(url=url):
                self.assertIn(self.client.get(url).status_code, (200, 503))
