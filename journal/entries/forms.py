from django import forms
from django.forms.widgets import Textarea

from entries.models import JournalEntryPage


class JournalEntryForm(forms.ModelForm):

    help_texts = {
        # Taha Hinengaro
        'mood': 'How did you feel today? (1 = low, 10 = great)',
        'anxiety_level': 'How anxious were you? (1 = calm, 10 = very anxious)',
        'stress_level': 'How stressed were you? (1 = relaxed, 10 = overwhelmed)',

        # Taha Tinana
        'sleep_hours': 'How many hours did you sleep?',
        'sleep_quality': 'How restful was your sleep? (1 = poor, 10 = excellent)',
        'exercise_level': 'How much did you move your body? (1 = sedentary, 10 = very active)',
        'diet_quality': 'How well did you eat? (1 = poorly, 10 = very healthy)',
        'energy_level': 'How energetic did you feel? (1 = exhausted, 10 = full of energy)',
        'alcohol_caffeine_consumption': 'Any alcohol or caffeine today?',

        # Taha Whānau
        'social_connection': 'How connected did you feel to others? (1 = isolated, 10 = deeply connected)',
        'social_interactions_quality': 'How were your interactions with people? (1 = difficult, 10 = meaningful)',

        # Taha Wairua
        'sense_of_meaning': 'Did today feel worthwhile? (1 = pointless, 10 = deeply meaningful)',

        # Mauriora
        'felt_like_myself': 'How much did you feel like yourself? (1 = not at all, 10 = completely)',

        # Waiora
        'environment_quality': 'Did your surroundings support your wellbeing? (1 = not at all, 10 = very supportive)',

        # Reflection
        'overall_day_rating': 'Overall, how was your day? (1 = terrible, 10 = amazing)',
        'best_thing_today': 'What was the best thing about today?',
        'hardest_thing_today': 'What was the hardest thing about today?',
        'significant_events': 'Any significant events?',
        'log': 'Write freely about your day...',
    }

    class Meta:
        model = JournalEntryPage
        fields = [
            'date',
            # Hinengaro
            'mood', 'anxiety_level', 'stress_level',
            # Tinana
            'sleep_hours', 'sleep_quality', 'exercise_level', 'diet_quality', 'energy_level',
            'alcohol_caffeine_consumption',
            # Whānau
            'social_connection', 'social_interactions_quality',
            # Wairua
            'sense_of_meaning',
            # Mauriora
            'felt_like_myself',
            # Waiora
            'environment_quality',
            # Reflection
            'overall_day_rating', 'best_thing_today', 'hardest_thing_today',
            'significant_events', 'log',
        ]
        widgets = {
            'date': forms.SelectDateWidget(),
            'best_thing_today': Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'What went well?'
            }),
            'hardest_thing_today': Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'What was challenging?'
            }),
            'significant_events': Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
            }),
            'log': Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write about your day, thoughts, feelings...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = self.help_texts.get(field_name, '')
