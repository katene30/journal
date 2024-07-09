from entries.models import JournalEntry
from django.forms import ModelForm

class EntryForm(ModelForm):
    class Meta:
        model = JournalEntry
        fields = '__all__'
