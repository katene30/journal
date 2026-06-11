from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.dateformat import DateFormat
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel

# Fields that use 1-10 slider input
SLIDER_FIELDS = [
    # Taha Hinengaro
    'mood', 'anxiety_level', 'stress_level',
    # Taha Tinana
    'sleep_quality', 'exercise_level', 'diet_quality', 'energy_level',
    # Taha Whānau
    'social_connection', 'social_interactions_quality',
    # Taha Wairua
    'sense_of_meaning',
    # Mauriora
    'felt_like_myself',
    # Waiora
    'environment_quality',
    # Reflection
    'overall_day_rating',
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
    generated_header = models.CharField(max_length=255, blank=True)

    # Taha Hinengaro - Mental and emotional wellbeing
    mood = models.IntegerField(null=True, blank=True)
    anxiety_level = models.IntegerField(null=True, blank=True)
    stress_level = models.IntegerField(null=True, blank=True)

    # Taha Tinana - Physical wellbeing
    sleep_hours = models.IntegerField(null=True, blank=True)
    sleep_quality = models.IntegerField(null=True, blank=True)
    exercise_level = models.IntegerField(null=True, blank=True)
    diet_quality = models.IntegerField(null=True, blank=True)
    energy_level = models.IntegerField(null=True, blank=True)
    alcohol_caffeine_consumption = models.CharField(max_length=255, blank=True)

    # Taha Whānau - Relationships and belonging
    social_connection = models.IntegerField(null=True, blank=True)
    social_interactions_quality = models.IntegerField(null=True, blank=True)

    # Taha Wairua - Meaning, purpose, spirituality
    sense_of_meaning = models.IntegerField(null=True, blank=True)

    # Mauriora - Identity (Te Pae Mahutonga)
    felt_like_myself = models.IntegerField(null=True, blank=True)

    # Waiora - Environment (Te Pae Mahutonga)
    environment_quality = models.IntegerField(null=True, blank=True)

    # Reflection
    overall_day_rating = models.IntegerField(null=True, blank=True)
    best_thing_today = models.TextField(blank=True)
    hardest_thing_today = models.TextField(blank=True)
    significant_events = models.TextField(blank=True)
    log = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('mood'),
                FieldPanel('anxiety_level'),
                FieldPanel('stress_level'),
            ]),
        ], heading="Taha Hinengaro - Mind"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('sleep_hours'),
                FieldPanel('sleep_quality'),
                FieldPanel('energy_level'),
            ]),
            FieldRowPanel([
                FieldPanel('exercise_level'),
                FieldPanel('diet_quality'),
            ]),
            FieldPanel('alcohol_caffeine_consumption'),
        ], heading="Taha Tinana - Body"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('social_connection'),
                FieldPanel('social_interactions_quality'),
            ]),
        ], heading="Taha Whānau - Family/Belonging"),
        MultiFieldPanel([
            FieldPanel('sense_of_meaning'),
        ], heading="Taha Wairua - Spirit"),
        MultiFieldPanel([
            FieldPanel('felt_like_myself'),
        ], heading="Mauriora - Identity"),
        MultiFieldPanel([
            FieldPanel('environment_quality'),
        ], heading="Waiora - Environment"),
        MultiFieldPanel([
            FieldPanel('overall_day_rating'),
            FieldPanel('best_thing_today'),
            FieldPanel('hardest_thing_today'),
            FieldPanel('significant_events'),
            FieldPanel('log'),
        ], heading="Reflection"),
    ]

    def generate_header(self):
        """Generate a simple header from the first few words of the log."""
        if self.log:
            words = self.log.split()[:5]
            self.generated_header = ' '.join(words) + ('...' if len(words) == 5 else '')
        else:
            self.generated_header = f"Entry for {self.date}"

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

        # Chart organized by pillar
        chart_labels = [
            # Hinengaro
            'Mood', 'Anxiety', 'Stress',
            # Tinana
            'Sleep Quality', 'Exercise', 'Diet', 'Energy',
            # Whānau
            'Connection', 'Interactions',
            # Wairua
            'Meaning',
            # Mauriora
            'Felt Like Myself',
            # Waiora
            'Environment',
            # Overall
            'Overall',
        ]

        chart_data = [
            # Hinengaro
            self.mood or 0,
            self.anxiety_level or 0,
            self.stress_level or 0,
            # Tinana
            self.sleep_quality or 0,
            self.exercise_level or 0,
            self.diet_quality or 0,
            self.energy_level or 0,
            # Whānau
            self.social_connection or 0,
            self.social_interactions_quality or 0,
            # Wairua
            self.sense_of_meaning or 0,
            # Mauriora
            self.felt_like_myself or 0,
            # Waiora
            self.environment_quality or 0,
            # Overall
            self.overall_day_rating or 0,
        ]

        chart_colors = [
            # Hinengaro (blues)
            '#2196F3', '#64B5F6', '#90CAF9',
            # Tinana (greens)
            '#4CAF50', '#66BB6A', '#81C784', '#A5D6A7',
            # Whānau (oranges)
            '#FF9800', '#FFB74D',
            # Wairua (purple)
            '#9C27B0',
            # Mauriora (pink)
            '#E91E63',
            # Waiora (teal)
            '#00BCD4',
            # Overall (gold)
            '#FFC107',
        ]

        context = self.get_context(request)
        context['entry'] = self
        context['form'] = form
        context['slider_fields'] = SLIDER_FIELDS
        context['chart_labels'] = chart_labels
        context['chart_data'] = chart_data
        context['chart_colors'] = chart_colors
        context['chart_id'] = 'journalEntryChart'
        context['chart_title'] = 'Hauora Overview'
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
                entry_page = JournalEntryPage(
                    user=request.user,
                    date=form.cleaned_data['date'],
                    # Hinengaro
                    mood=form.cleaned_data.get('mood'),
                    anxiety_level=form.cleaned_data.get('anxiety_level'),
                    stress_level=form.cleaned_data.get('stress_level'),
                    # Tinana
                    sleep_hours=form.cleaned_data.get('sleep_hours'),
                    sleep_quality=form.cleaned_data.get('sleep_quality'),
                    exercise_level=form.cleaned_data.get('exercise_level'),
                    diet_quality=form.cleaned_data.get('diet_quality'),
                    energy_level=form.cleaned_data.get('energy_level'),
                    alcohol_caffeine_consumption=form.cleaned_data.get('alcohol_caffeine_consumption', ''),
                    # Whānau
                    social_connection=form.cleaned_data.get('social_connection'),
                    social_interactions_quality=form.cleaned_data.get('social_interactions_quality'),
                    # Wairua
                    sense_of_meaning=form.cleaned_data.get('sense_of_meaning'),
                    # Mauriora
                    felt_like_myself=form.cleaned_data.get('felt_like_myself'),
                    # Waiora
                    environment_quality=form.cleaned_data.get('environment_quality'),
                    # Reflection
                    overall_day_rating=form.cleaned_data.get('overall_day_rating'),
                    best_thing_today=form.cleaned_data.get('best_thing_today', ''),
                    hardest_thing_today=form.cleaned_data.get('hardest_thing_today', ''),
                    significant_events=form.cleaned_data.get('significant_events', ''),
                    log=form.cleaned_data.get('log', ''),
                )

                entry_page.generate_header()
                entry_page.title = entry_page.generated_header or f"Entry for {entry_page.date}"
                entry_page.slug = f"entry-{entry_page.date}"

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
        # Hinengaro
        'mood': 'Mood',
        'anxiety_level': 'Anxiety Level',
        'stress_level': 'Stress Level',
        # Tinana
        'sleep_quality': 'Sleep Quality',
        'exercise_level': 'Exercise Level',
        'diet_quality': 'Diet Quality',
        'energy_level': 'Energy Level',
        # Whānau
        'social_connection': 'Social Connection',
        'social_interactions_quality': 'Social Interactions Quality',
        # Wairua
        'sense_of_meaning': 'Sense of Meaning',
        # Mauriora
        'felt_like_myself': 'Felt Like Myself',
        # Waiora
        'environment_quality': 'Environment Quality',
        # Overall
        'overall_day_rating': 'Overall Day Rating',
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
