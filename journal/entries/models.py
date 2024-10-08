from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.dateformat import DateFormat
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

SLIDER_FIELDS = [
            'mood', 'depression_level', 'anxiety_level', 'stress_level', 
            'sleep_quality', 'energy_level', 
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
    hero_alt_text = models.CharField(max_length=255, blank=True, help_text="Alt text for the hero image")
    body = RichTextField(blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )



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
        
        # Prepare data for the bar chart
        chart_labels = [
            'Mood', 'Depression Level', 'Anxiety Level', 'Stress Level',
            'Sleep Quality', 'Energy Level', 'Social Interactions Quality',
            'Productivity Level', 'Diet Quality', 'Self-care Effectiveness',
            'Overall Day Rating'
        ]

        chart_data = [
            self.journal_entry.mood,
            self.journal_entry.depression_level,
            self.journal_entry.anxiety_level,
            self.journal_entry.stress_level,
            self.journal_entry.sleep_quality or 0,
            self.journal_entry.energy_level,
            self.journal_entry.social_interactions_quality or 0,
            self.journal_entry.productivity_level or 0,
            self.journal_entry.diet_quality or 0,
            self.journal_entry.self_care_effectiveness,
            self.journal_entry.overall_day_rating
        ]

        chart_colors = ['#4CAF50', '#2196F3', '#FF9800', '#F44336', '#3F51B5',
                '#FFC107', '#9C27B0', '#00BCD4', '#8BC34A', '#E91E63', '#FF5722']


        context = self.get_context(request)
        context['entry'] = self.journal_entry
        context['form'] = form
        context['slider_fields'] = SLIDER_FIELDS
        context['chart_labels'] = chart_labels
        context['chart_data'] = chart_data
        context['chart_colors'] = chart_colors
        context['chart_id'] = 'journalEntryChart'
        context['chart_title'] = 'Daily Metrics Overview'
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

from wagtail.models import Page
from django.db import models
from wagtail.admin.panels import FieldPanel
from django.shortcuts import render
from entries.models import JournalEntry

class SummaryPage(Page):
    intro_text = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro_text'),
    ]

    METRIC_LABELS = {
        'mood': 'Mood',
        'depression_level': 'Depression Level',
        'anxiety_level': 'Anxiety Level',
        'stress_level': 'Stress Level',
        'sleep_quality': 'Sleep Quality',
        'energy_level': 'Energy Level',
        'social_interactions_quality': 'Social Interactions Quality',
        'productivity_level': 'Productivity Level',
        'diet_quality': 'Diet Quality',
        'self_care_effectiveness': 'Self-care Effectiveness',
        'overall_day_rating': 'Overall Day Rating'
    }

    def serve(self, request):
        # Get filters from the request
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        metric = request.GET.get('metric', 'overall_day_rating')

        # Fetch entries based on filters
        journal_entries = JournalEntry.objects.filter(
            user=request.user,
            date__range=[start_date, end_date]
        ).order_by('date')

        # Prepare data for the chart
        dates = [DateFormat(entry.date).format('Y-m-d') for entry in journal_entries]
        values = [getattr(entry, metric) for entry in journal_entries]

        available_metric_labels = [
            (key, self.METRIC_LABELS[key])
            for key in self.METRIC_LABELS
        ]

        context = self.get_context(request)
        context['dates'] = dates
        context['values'] = values
        context['metric'] = metric
        context['metric_label'] = self.METRIC_LABELS.get(metric, metric)
        context['available_metrics'] = [key for key in self.METRIC_LABELS.keys()]
        context['available_metric_labels'] = available_metric_labels
        return render(request, 'entries/summary_page.html', context)
