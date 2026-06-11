from django import forms
from django.forms.widgets import Textarea

from entries.models import JournalEntryPage


class JournalEntryForm(forms.ModelForm):

    help_texts = {
        'mood': 'How did you feel today? Rate your overall mood from 1 (feeling blue) to 10 (over the moon)!',
        'depression_level': 'Feeling down or out? Rate your depression level from 1 (not at all) to 10 (extremely).',
        'anxiety_level': 'How anxious were you today? Rate your anxiety level from 1 (calm) to 10 (on edge).',
        'stress_level': 'How much stress did you feel? Rate your stress level from 1 (chilled out) to 10 (stressed out).',
        'sleep_hours': 'How many hours of beauty sleep did you get last night? Be honest!',
        'sleep_quality': 'How restful was your sleep? Rate from 1 (tossing and turning) to 10 (slept like a baby).',
        'energy_level': 'How energetic did you feel today? Rate from 1 (drained) to 10 (supercharged).',
        'social_interactions_quality': 'How were your social interactions? Rate from 1 (awkward) to 10 (amazing).',
        'productivity_level': 'How productive were you? Rate from 1 (procrastinated) to 10 (got things done).',
        'diet_quality': 'How would you rate your diet today? From 1 (junk food overload) to 10 (super healthy).',
        'alcohol_caffeine_consumption': 'How much alcohol or caffeine did you consume? Share your drink count!',
        'self_care_effectiveness': 'How well did you take care of yourself? Rate from 1 (neglected) to 10 (self-care superstar).',
        'significant_events': 'Any significant events today? Share the highlights or lowlights!',
        'overall_day_rating': 'Overall, how was your day? Rate from 1 (terrible) to 10 (fantastic).',
    }

    class Meta:
        model = JournalEntryPage
        fields = [
            'date', 'log',
            'mood', 'depression_level', 'anxiety_level', 'stress_level',
            'sleep_hours', 'sleep_quality', 'energy_level',
            'social_interactions_quality', 'productivity_level', 'diet_quality',
            'alcohol_caffeine_consumption', 'self_care_effectiveness',
            'significant_events', 'overall_day_rating',
        ]
        widgets = {
            'log': Textarea(attrs={
                'class': "form-control",
                'placeholder': "Write about your day, thoughts, feelings, and significant events here..."
            }),
            'significant_events': Textarea(attrs={
                'class': "form-control",
            }),
            'date': forms.SelectDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = self.help_texts.get(field_name, '')
