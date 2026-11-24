"""Create a local demo account with ~10 weeks of realistic journal entries.

    python manage.py seed_demo
    python manage.py seed_demo --email you@example.com --days 120

Re-running replaces that account's entries. Refuses to run unless DEBUG is on,
so it can't be pointed at the production database by accident.
"""
import math
import random
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from entries.models import JournalEntry

BEST = [
    'Kai with my cousins after church.',
    'Long walk along the waterfront at lunch, sun was out.',
    'Finished the report I had been dreading.',
    'My niece called just to say hi.',
    'Got to the gym before work for once.',
    'Cooked a proper dinner instead of takeaways.',
    'Quiet morning coffee on the deck.',
    'Kapa haka practice, felt really connected.',
    'Good catch-up with Mum on the phone.',
    'Swam at the beach, freezing but worth it.',
    'Read a whole chapter without looking at my phone.',
    'Helped my neighbour with their garden.',
    'Team meeting actually went well.',
    'Slept in and did not feel guilty about it.',
    'Karakia with the whānau before dinner.',
]
HARD = [
    'Running on empty all afternoon.',
    'Back-to-back meetings, no time to think.',
    'Did not sleep well, kept waking up.',
    'Felt a bit isolated working from home all day.',
    'Argument with my partner about money.',
    'Too much screen time, felt flat.',
    'Deadline pressure at work.',
    'Missed training again.',
    'Headache most of the day.',
    'Traffic was terrible both ways.',
    'Hard to switch off at night.',
    'Felt behind on everything.',
]
EVENTS = [
    "Whānau dinner at Nan's.",
    'Started a new project at work.',
    "Doctor's appointment.",
    'Matariki long weekend.',
    "Friend's birthday drinks.",
    'Car in for a service.',
    'Tangi for a family friend.',
    'Moved my desk to the window.',
]
JOURNAL = [
    'Tired today but not stressed. Need an early night.',
    'Pretty ordinary day. Work, gym, dinner, bed. Nothing big, nothing bad.',
    'Feeling more like myself again after a rough week. Getting outside helped a lot.',
    'Busy and a bit scattered. I keep saying yes to things and then running out of time for myself.',
    'Good day overall. Spent the evening with whānau and laughed a lot.',
    'Struggled to get going this morning. Things picked up after lunch once I got some fresh air.',
    'Noticed I feel better on the days I move my body, even just a short walk.',
    'Quiet one. Read, cooked, early night. Exactly what I needed.',
    'Stressful at work but I handled it better than last time.',
    'Feeling grateful for my people today.',
    'Low energy, not much to say. Tomorrow is another day.',
    'Felt connected at church this morning. Carried that calm through the day.',
]
GRATITUDE = [
    'My bed. Hot shower. Mum checking in.',
    'Sunshine on the walk to work.',
    'A good laugh with my cousins.',
    'Leftovers so I did not have to cook.',
    'My health, even on a slow day.',
    'Karakia this morning, it settled me.',
    'A friend who listened without fixing.',
    'Fresh kai from the garden.',
    'Getting through a hard day.',
]
CAFFEINE = ['1 coffee', '2 coffees', '3 coffees', '1 coffee, 1 wine', 'tea only', '2 coffees, 2 beers', '']
CHURCH_BEST, CHURCH_JOURNAL = BEST[0], JOURNAL[-1]


class Command(BaseCommand):
    help = 'Create a local demo account with realistic journal entries (DEBUG only).'

    def add_arguments(self, parser):
        parser.add_argument('--email', default='test@example.com')
        parser.add_argument('--password', default='Test-pass-123!')
        parser.add_argument('--days', type=int, default=70, help='How many days back to fill (default 70)')
        parser.add_argument('--seed', type=int, default=2026, help='Random seed, for repeatable data')

    def handle(self, *args, email, password, days, seed, **options):
        if not settings.DEBUG:
            raise CommandError('seed_demo only runs with DEBUG on, to keep demo data out of production.')
        if days < 1:
            raise CommandError('--days must be at least 1.')

        rng = random.Random(seed)
        with transaction.atomic():
            user, _ = User.objects.get_or_create(username=email, defaults={'email': email})
            user.email = email
            user.set_password(password)
            user.save()
            user.entries.all().delete()
            entries = [self.make_entry(rng, user, i) for i in range(days)]
            JournalEntry.objects.bulk_create([e for e in entries if e])

        count = user.entries.count()
        self.stdout.write(self.style.SUCCESS(
            f'{email}: {count} entries over the last {days} days (password: {password})'
        ))

    def make_entry(self, rng, user, i):
        def rate(base, spread=0.8):
            return max(1, min(5, round(base + rng.uniform(-spread, spread))))

        def maybe(value, chance):
            return value if rng.random() < chance else None

        day = timezone.localdate() - timedelta(days=i)
        # About one day in six is skipped (never today)
        if i > 0 and rng.random() < 0.16:
            return None

        weekend = day.weekday() >= 5
        sunday = day.weekday() == 6
        # A slow wave of better and harder weeks, plus a tough stretch 3-4 weeks ago
        wave = math.sin(i / 7)
        tough = 1.0 if 18 <= i <= 27 else 0.0

        sleep_q = rate(3.3 - 0.6 * tough + 0.3 * weekend)
        energy = rate((sleep_q + 3) / 2 + 0.2 * wave)
        stress = rate(2.6 + 1.3 * tough - 0.6 * weekend + 0.3 * wave)
        mood = rate(3.4 - 0.9 * tough + 0.4 * weekend - 0.3 * wave)
        connection = rate(3.2 + 0.9 * weekend - 0.4 * tough)
        # Some days only the main sliders get filled in
        light = rng.random() < 0.2

        entry = JournalEntry(
            user=user,
            date=day,
            overall_day_rating=rate((mood + energy + 6 - stress) / 3),
            mood=mood,
            anxiety_level=rate(2.4 + 1.0 * tough + 0.2 * wave),
            stress_level=stress,
            sleep_hours=max(4, min(10, round(7 + (sleep_q - 3) * 0.8 + rng.uniform(-1, 1)))),
            sleep_quality=sleep_q,
            energy_level=energy,
            exercise_level=maybe(rate(2.8 + 0.5 * weekend), 0.85),
            diet_quality=maybe(rate(3.3 - 0.4 * tough), 0.85),
            alcohol_caffeine_consumption=rng.choice(CAFFEINE),
            social_connection=connection,
            social_interactions_quality=None if light else maybe(rate(connection + 0.2), 0.85),
            sense_of_meaning=rate(3.1 - 0.5 * tough + 0.4 * sunday),
            spiritual_connection=None if light else maybe(rate(3.0 + 1.2 * sunday), 0.75),
            felt_like_myself=rate(3.4 - 0.8 * tough),
            environment_quality=maybe(rate(3.5 + 0.3 * weekend), 0.8),
        )
        if not light:
            entry.gratitude = maybe(rng.choice(GRATITUDE), 0.7) or ''
            entry.best_thing_today = CHURCH_BEST if sunday and rng.random() < 0.5 else rng.choice(BEST)
            entry.hardest_thing_today = maybe(rng.choice(HARD), 0.8) or ''
            entry.significant_events = maybe(rng.choice(EVENTS), 0.25) or ''
            entry.log = CHURCH_JOURNAL if sunday and rng.random() < 0.5 else rng.choice(JOURNAL)
        return entry
