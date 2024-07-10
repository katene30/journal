from entries.models import JournalEntry
from django.forms import ModelForm
from django.forms.widgets import Textarea
from datetime import date


class EntryForm(ModelForm):
    class Meta:
        model = JournalEntry
        exclude = ['user','date','generated_header']
        widgets = {
            'log': Textarea(attrs={
                'class': "form-control",
                'placeholder': "Write about your day, thoughts, feelings, and significant events here..."
                }),
            'significant_events': Textarea(attrs={
                'class': "form-control",
                }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        instance.date = date.today()
        if commit:
            instance.generate_header()
            instance.save()
        return instance