from rest_framework import serializers
from .models import JournalEntry


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
            # Mauriora
            'felt_like_myself',
            # Waiora
            'environment_quality',
            # Reflection
            'overall_day_rating',
            'best_thing_today',
            'hardest_thing_today',
            'significant_events',
            'log',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class JournalEntryListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views."""
    header = serializers.ReadOnlyField()

    class Meta:
        model = JournalEntry
        fields = ['id', 'date', 'header', 'overall_day_rating', 'mood', 'log']
