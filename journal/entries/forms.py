from entries.models import JournalEntry
from django.forms import ModelForm
from datetime import date


class EntryForm(ModelForm):
    class Meta:
        model = JournalEntry
        exclude = ['user','date']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        instance.date = date.today()
        if commit:
            instance.save()
        return instance