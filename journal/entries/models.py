from django.db import models
from django.contrib.auth.models import User


class JournalEntry(models.Model):
    """A daily journal entry tracking hauora (wellbeing) metrics."""

    # Entry metadata
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Taha Hinengaro - Mental and emotional wellbeing
    mood = models.IntegerField(null=True, blank=True)
    anxiety_level = models.IntegerField(null=True, blank=True)
    stress_level = models.IntegerField(null=True, blank=True)

    # Taha Tinana - Physical wellbeing
    sleep_hours = models.IntegerField(null=True, blank=True)
    sleep_quality = models.IntegerField(null=True, blank=True)
    exercise_level = models.IntegerField(null=True, blank=True)
    diet_quality = models.IntegerField(null=True, blank=True)
    energy_level = models.IntegerField(null=True, blank=True)
    alcohol_caffeine_consumption = models.CharField(max_length=255, blank=True)

    # Taha Whānau - Relationships and belonging
    social_connection = models.IntegerField(null=True, blank=True)
    social_interactions_quality = models.IntegerField(null=True, blank=True)

    # Taha Wairua - Meaning, purpose, spirituality
    sense_of_meaning = models.IntegerField(null=True, blank=True)
    # Optional: faith, karakia, nature, whakapapa, whatever feeds the spirit
    spiritual_connection = models.IntegerField(null=True, blank=True)

    # Mauriora - Identity (Te Pae Mahutonga)
    felt_like_myself = models.IntegerField(null=True, blank=True)

    # Waiora - Environment (Te Pae Mahutonga)
    environment_quality = models.IntegerField(null=True, blank=True)

    # Reflection
    overall_day_rating = models.IntegerField(null=True, blank=True)
    best_thing_today = models.TextField(blank=True)
    hardest_thing_today = models.TextField(blank=True)
    significant_events = models.TextField(blank=True)
    log = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'journal entries'
        ordering = ['-date']
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.date} - {self.user.username}"

    def get_absolute_url(self):
        # Used by Django admin's "View on site" link
        return f'/app/entries/{self.pk}'

    def generate_header(self):
        """Generate a simple header from the first few words of the log."""
        if self.log:
            words = self.log.split()[:5]
            return ' '.join(words) + ('...' if len(words) == 5 else '')
        return f"Entry for {self.date}"

    @property
    def header(self):
        return self.generate_header()


# Fields rated on a 1-5 semantic scale
SLIDER_FIELDS = [
    # Taha Hinengaro
    'mood', 'anxiety_level', 'stress_level',
    # Taha Tinana
    'sleep_quality', 'exercise_level', 'diet_quality', 'energy_level',
    # Taha Whānau
    'social_connection', 'social_interactions_quality',
    # Taha Wairua
    'sense_of_meaning', 'spiritual_connection',
    # Mauriora
    'felt_like_myself',
    # Waiora
    'environment_quality',
    # Reflection
    'overall_day_rating',
]
