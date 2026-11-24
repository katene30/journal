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


# Free-text fields: the private part of an entry
REFLECTION_TEXT_FIELDS = ['log', 'gratitude', 'best_thing_today', 'hardest_thing_today', 'significant_events']
PREVIEW_LENGTH = 120


class JournalEntryListSerializer(serializers.ModelSerializer):
    """Entry tiles: the date and the ratings, never the journal text.

    Lists are glanceable, so they leave out what someone wrote. `preview`
    (the start of the first Reflection box written in) is only filled in when the request asks for
    it with ?preview=1, which the app sends when the person has turned
    journal previews on.
    """
    has_reflection = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()

    class Meta:
        model = JournalEntry
        fields = ['id', 'date', 'overall_day_rating', *SLIDER_FIELDS, 'has_reflection', 'preview']

    def get_has_reflection(self, entry):
        return any(getattr(entry, field).strip() for field in REFLECTION_TEXT_FIELDS)

    def get_preview(self, entry):
        request = self.context.get('request')
        if not request or request.query_params.get('preview') != '1':
            return None
        return preview_text(entry)


def preview_text(entry):
    """The start of the first Reflection box that has something in it."""
    text = next((getattr(entry, f).strip() for f in REFLECTION_TEXT_FIELDS if getattr(entry, f).strip()), '')
    if len(text) <= PREVIEW_LENGTH:
        return text
    return text[:PREVIEW_LENGTH].rstrip() + '…'


class JournalEntryScalesSerializer(serializers.ModelSerializer):
    """Date plus every 1-5 scale value, for the summary charts."""

    class Meta:
        model = JournalEntry
        fields = ['id', 'date', *SLIDER_FIELDS]
