from rest_framework import serializers
from .models import JournalEntry, SLIDER_FIELDS


class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = [
            'id',
            'date',
            'created_at',
            'updated_at',
            # Hinengaro
            'mood',
            'anxiety_level',
            'stress_level',
            # Tinana
            'sleep_hours',
            'sleep_quality',
            'exercise_level',
            'diet_quality',
            'energy_level',
            'alcohol_caffeine_consumption',
            # Whanau
            'social_connection',
            'social_interactions_quality',
            # Wairua
            'sense_of_meaning',
            'spiritual_connection',
            # Mauriora
            'felt_like_myself',
            # Waiora
            'environment_quality',
            # Reflection
            'overall_day_rating',
            'log',
            'gratitude',
            'best_thing_today',
            'hardest_thing_today',
            'significant_events',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        # Pillar scores and charts assume every slider is 1-5
        extra_kwargs = {field: {'min_value': 1, 'max_value': 5} for field in SLIDER_FIELDS}


class JournalEntryListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views."""
    header = serializers.ReadOnlyField()

    class Meta:
        model = JournalEntry
        fields = ['id', 'date', 'header', 'overall_day_rating', 'mood', 'log']


class JournalEntryScalesSerializer(serializers.ModelSerializer):
    """Date plus every 1-5 scale value, for the summary charts."""

    class Meta:
        model = JournalEntry
        fields = ['id', 'date', *SLIDER_FIELDS]
