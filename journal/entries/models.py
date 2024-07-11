from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

SLIDER_FIELDS = [
            'mood', 'depression_level', 'anxiety_level', 'stress_level', 
            'sleep_hours', 'sleep_quality', 'energy_level', 
            'social_interactions_quality', 'productivity_level', 
            'diet_quality', 'self_care_effectiveness', 'overall_day_rating'
        ]

@register_snippet
class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    log = models.TextField()
    generated_header = models.CharField(max_length=255, blank=True, null=True)
    mood = models.IntegerField()
    depression_level = models.IntegerField()
    anxiety_level = models.IntegerField()
    stress_level = models.IntegerField()
    sleep_hours = models.IntegerField(blank=True, null=True)
    sleep_quality = models.IntegerField(blank=True, null=True)
    energy_level = models.IntegerField()
    social_interactions_quality = models.IntegerField(blank=True, null=True)
    productivity_level = models.IntegerField(blank=True, null=True)
    diet_quality = models.IntegerField(blank=True, null=True)
    alcohol_caffeine_consumption = models.CharField(max_length=255, blank=True, null=True)
    self_care_effectiveness = models.IntegerField()
    significant_events = models.TextField(blank=True, null=True)
    overall_day_rating = models.IntegerField()
    entry_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Entry for {self.user} on {self.date}"
    
    class Meta:
        verbose_name_plural = "journal entries"
    
    def generate_header(self):
        import cohere
        co = cohere.Client(settings.COHERE_API_KEY)

        response = co.chat(
            message=f'Generate a fun and creative header for the following journal entry log in five words or less. Make sure to only include the heading with no other text:\n\n{self.log}',
        )

        self.generated_header = response.text
        self.save()

class HomePage(Page):
    header_text = models.CharField(max_length=255, blank=True)
    hero_image = models.ImageField(blank=True)
    hero_alt_text = models.CharField(max_length=255, blank=True, help_text="Alt text for the hero image")
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header_text'),
        FieldPanel('hero_image'),
        FieldPanel('hero_alt_text'),
        FieldPanel('body'),
    ]

class JournalEntryPage(Page):
    journal_entry = models.ForeignKey('JournalEntry', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    content_panels = Page.content_panels + [
        FieldPanel('journal_entry'),
    ]

    def serve(self, request):
        from entries.forms import EntryForm
        if request.method == 'POST':

            if 'delete_button' in request.POST:
                if self.journal_entry:
                    self.journal_entry.delete()
                    return redirect(self.get_parent().url) 

            form = EntryForm(request.POST, instance=self.journal_entry)
            if form.is_valid():
                form.save()
                return redirect(self.url)
        else:
            form = EntryForm(instance=self.journal_entry)

        context = self.get_context(request)
        context['entry'] = self.journal_entry
        context['form'] = form
        context['slider_fields'] = SLIDER_FIELDS
        return render(request, 'entries/journal_entry_page.html', context)

class JournalEntryFormPage(Page):
    intro_text = models.CharField(max_length=255, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro_text'),
    ]

    def serve(self, request, *args, **kwargs):
        from entries.forms import EntryForm
        if request.method == 'POST':
            form = EntryForm(request.POST, user=request.user)
            if form.is_valid():
                form.save()
                return redirect(self.url)
        else:
            form = EntryForm()
        
        return render(request, 'entries/journal_entry_form_page.html', {'form': form, 'slider_fields': SLIDER_FIELDS})
