import logging

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.dateformat import DateFormat
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel

logger = logging.getLogger(__name__)

SLIDER_FIELDS = [
    'mood', 'depression_level', 'anxiety_level', 'stress_level',
    'sleep_quality', 'energy_level',
    'social_interactions_quality', 'productivity_level',
    'diet_quality', 'self_care_effectiveness', 'overall_day_rating'
]


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
    # Entry metadata
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    log = models.TextField(blank=True)
    generated_header = models.CharField(max_length=255, blank=True)

    # Metrics
    mood = models.IntegerField(null=True, blank=True)
    depression_level = models.IntegerField(null=True, blank=True)
    anxiety_level = models.IntegerField(null=True, blank=True)
    stress_level = models.IntegerField(null=True, blank=True)
    sleep_hours = models.IntegerField(null=True, blank=True)
    sleep_quality = models.IntegerField(null=True, blank=True)
    energy_level = models.IntegerField(null=True, blank=True)
    social_interactions_quality = models.IntegerField(null=True, blank=True)
    productivity_level = models.IntegerField(null=True, blank=True)
    diet_quality = models.IntegerField(null=True, blank=True)
    alcohol_caffeine_consumption = models.CharField(max_length=255, blank=True)
    self_care_effectiveness = models.IntegerField(null=True, blank=True)
    significant_events = models.TextField(blank=True)
    overall_day_rating = models.IntegerField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('log'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('mood'),
                FieldPanel('depression_level'),
                FieldPanel('anxiety_level'),
                FieldPanel('stress_level'),
            ]),
            FieldRowPanel([
                FieldPanel('sleep_hours'),
                FieldPanel('sleep_quality'),
                FieldPanel('energy_level'),
            ]),
            FieldRowPanel([
                FieldPanel('social_interactions_quality'),
                FieldPanel('productivity_level'),
                FieldPanel('diet_quality'),
            ]),
            FieldRowPanel([
                FieldPanel('self_care_effectiveness'),
                FieldPanel('overall_day_rating'),
            ]),
        ], heading="Metrics"),
        FieldPanel('alcohol_caffeine_consumption'),
        FieldPanel('significant_events'),
    ]

    def generate_header(self):
        import cohere

        try:
            co = cohere.Client(settings.COHERE_API_KEY)
            response = co.chat(
                message=f'Generate a fun and creative header for the following journal entry log in five words or less. Make sure to only include the heading with no other text:\n\n{self.log}',
            )
            self.generated_header = response.text
        except Exception as e:
            logger.warning(f"Failed to generate header via Cohere: {e}")
            words = self.log.split()[:5]
            self.generated_header = ' '.join(words) + ('...' if len(self.log.split()) > 5 else '')

    def serve(self, request):
        from entries.forms import JournalEntryForm

        if request.method == 'POST':
            if 'delete_button' in request.POST:
                parent = self.get_parent()
                self.delete()
                return redirect(parent.url)

            form = JournalEntryForm(request.POST, instance=self)
            if form.is_valid():
                form.save()
                return redirect(self.url)
        else:
            form = JournalEntryForm(instance=self)

        chart_labels = [
            'Mood', 'Depression Level', 'Anxiety Level', 'Stress Level',
            'Sleep Quality', 'Energy Level', 'Social Interactions Quality',
            'Productivity Level', 'Diet Quality', 'Self-care Effectiveness',
            'Overall Day Rating'
        ]

        chart_data = [
            self.mood or 0,
            self.depression_level or 0,
            self.anxiety_level or 0,
            self.stress_level or 0,
            self.sleep_quality or 0,
            self.energy_level or 0,
            self.social_interactions_quality or 0,
            self.productivity_level or 0,
            self.diet_quality or 0,
            self.self_care_effectiveness or 0,
            self.overall_day_rating or 0
        ]

        chart_colors = [
            '#4CAF50', '#2196F3', '#FF9800', '#F44336', '#3F51B5',
            '#FFC107', '#9C27B0', '#00BCD4', '#8BC34A', '#E91E63', '#FF5722'
        ]

        context = self.get_context(request)
        context['entry'] = self
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
        from entries.forms import JournalEntryForm
        from wagtail.models import Site

        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')

        if request.method == 'POST':
            form = JournalEntryForm(request.POST)
            if form.is_valid():
                # Create the page directly
                entry_page = JournalEntryPage(
                    user=request.user,
                    date=form.cleaned_data['date'],
                    log=form.cleaned_data['log'],
                    mood=form.cleaned_data['mood'],
                    depression_level=form.cleaned_data['depression_level'],
                    anxiety_level=form.cleaned_data['anxiety_level'],
                    stress_level=form.cleaned_data['stress_level'],
                    sleep_hours=form.cleaned_data.get('sleep_hours'),
                    sleep_quality=form.cleaned_data.get('sleep_quality'),
                    energy_level=form.cleaned_data['energy_level'],
                    social_interactions_quality=form.cleaned_data.get('social_interactions_quality'),
                    productivity_level=form.cleaned_data.get('productivity_level'),
                    diet_quality=form.cleaned_data.get('diet_quality'),
                    alcohol_caffeine_consumption=form.cleaned_data.get('alcohol_caffeine_consumption', ''),
                    self_care_effectiveness=form.cleaned_data['self_care_effectiveness'],
                    significant_events=form.cleaned_data.get('significant_events', ''),
                    overall_day_rating=form.cleaned_data['overall_day_rating'],
                )

                # Generate AI header
                entry_page.generate_header()

                # Set page title and slug
                entry_page.title = entry_page.generated_header or f"Entry for {entry_page.date}"
                entry_page.slug = f"entry-{entry_page.date}"

                # Add as child of homepage
                homepage = Site.objects.first().root_page
                homepage.add_child(instance=entry_page)

                return redirect(entry_page.url)
        else:
            form = JournalEntryForm()

        return render(request, 'entries/journal_entry_form_page.html', {
            'form': form,
            'slider_fields': SLIDER_FIELDS
        })


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
        from datetime import date, timedelta

        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        metric = request.GET.get('metric', 'overall_day_rating')

        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = date.today() - timedelta(days=30)

        # Query JournalEntryPage instead of JournalEntry snippet
        entries = JournalEntryPage.objects.live().filter(
            user=request.user,
            date__range=[start_date, end_date]
        ).order_by('date')

        dates = [DateFormat(entry.date).format('Y-m-d') for entry in entries]
        values = [getattr(entry, metric) or 0 for entry in entries]

        available_metric_labels = [
            (key, self.METRIC_LABELS[key])
            for key in self.METRIC_LABELS
        ]

        context = self.get_context(request)
        context['dates'] = dates
        context['values'] = values
        context['metric'] = metric
        context['metric_label'] = self.METRIC_LABELS.get(metric, metric)
        context['available_metrics'] = list(self.METRIC_LABELS.keys())
        context['available_metric_labels'] = available_metric_labels
        return render(request, 'entries/summary_page.html', context)
