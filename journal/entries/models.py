from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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

    def __str__(self):
        return f"{self.date} - {self.user.username}"

    def get_absolute_url(self):
        return reverse('entry_detail', kwargs={'pk': self.pk})

    def generate_header(self):
        """Generate a simple header from the first few words of the log."""
        if self.log:
            words = self.log.split()[:5]
            return ' '.join(words) + ('...' if len(words) == 5 else '')
        return f"Entry for {self.date}"

    @property
    def header(self):
        return self.generate_header()


# Fields that use 1-10 slider input
SLIDER_FIELDS = [
    # Taha Hinengaro
    'mood', 'anxiety_level', 'stress_level',
    # Taha Tinana
    'sleep_quality', 'exercise_level', 'diet_quality', 'energy_level',
    # Taha Whānau
    'social_connection', 'social_interactions_quality',
    # Taha Wairua
    'sense_of_meaning',
    # Mauriora
    'felt_like_myself',
    # Waiora
    'environment_quality',
    # Reflection
    'overall_day_rating',
]

METRIC_LABELS = {
    # Hinengaro
    'mood': 'Mood',
    'anxiety_level': 'Anxiety Level',
    'stress_level': 'Stress Level',
    # Tinana
    'sleep_quality': 'Sleep Quality',
    'exercise_level': 'Exercise Level',
    'diet_quality': 'Diet Quality',
    'energy_level': 'Energy Level',
    # Whānau
    'social_connection': 'Social Connection',
    'social_interactions_quality': 'Social Interactions Quality',
    # Wairua
    'sense_of_meaning': 'Sense of Meaning',
    # Mauriora
    'felt_like_myself': 'Felt Like Myself',
    # Waiora
    'environment_quality': 'Environment Quality',
    # Overall
    'overall_day_rating': 'Overall Day Rating',
}
