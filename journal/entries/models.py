from django.db import models
from django.contrib.auth.models import User
from wagtail.fields import RichTextField

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    log = RichTextField()
    mood = models.IntegerField()
    depression_level = models.IntegerField()
    anxiety_level = models.IntegerField()
    stress_level = models.IntegerField()
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=1)
    sleep_quality = models.IntegerField()
    energy_level = models.IntegerField()
    social_interactions_quality = models.IntegerField()
    productivity_level = models.IntegerField()
    diet_quality = models.IntegerField()
    alcohol_caffeine_consumption = models.CharField(max_length=255, blank=True)
    self_care_effectiveness = models.IntegerField()
    significant_events = models.TextField(blank=True)
    overall_day_rating = models.IntegerField()

    def __str__(self):
        return f"Entry for {self.user} on {self.date}"
