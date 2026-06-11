from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import JournalEntry, SLIDER_FIELDS, METRIC_LABELS
from .forms import JournalEntryForm


def home(request):
    """Home page showing recent entries for logged-in users."""
    if request.user.is_authenticated:
        entries = JournalEntry.objects.filter(user=request.user)[:10]
    else:
        entries = []

    return render(request, 'entries/home.html', {
        'entries': entries,
    })


class EntryListView(LoginRequiredMixin, ListView):
    """List all entries for the current user."""
    model = JournalEntry
    template_name = 'entries/entry_list.html'
    context_object_name = 'entries'
    paginate_by = 20

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)


class EntryDetailView(LoginRequiredMixin, DetailView):
    """View a single entry with chart."""
    model = JournalEntry
    template_name = 'entries/entry_detail.html'
    context_object_name = 'entry'

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = self.object

        # Chart data organized by pillar
        context['chart_labels'] = [
            'Mood', 'Anxiety', 'Stress',
            'Sleep Quality', 'Exercise', 'Diet', 'Energy',
            'Connection', 'Interactions',
            'Meaning',
            'Felt Like Myself',
            'Environment',
            'Overall',
        ]

        context['chart_data'] = [
            entry.mood or 0,
            entry.anxiety_level or 0,
            entry.stress_level or 0,
            entry.sleep_quality or 0,
            entry.exercise_level or 0,
            entry.diet_quality or 0,
            entry.energy_level or 0,
            entry.social_connection or 0,
            entry.social_interactions_quality or 0,
            entry.sense_of_meaning or 0,
            entry.felt_like_myself or 0,
            entry.environment_quality or 0,
            entry.overall_day_rating or 0,
        ]

        context['chart_colors'] = [
            '#2196F3', '#64B5F6', '#90CAF9',  # Hinengaro (blues)
            '#4CAF50', '#66BB6A', '#81C784', '#A5D6A7',  # Tinana (greens)
            '#FF9800', '#FFB74D',  # Whānau (oranges)
            '#9C27B0',  # Wairua (purple)
            '#E91E63',  # Mauriora (pink)
            '#00BCD4',  # Waiora (teal)
            '#FFC107',  # Overall (gold)
        ]

        return context


class EntryCreateView(LoginRequiredMixin, CreateView):
    """Create a new entry."""
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'entries/entry_form.html'

    def get_initial(self):
        return {'date': date.today()}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider_fields'] = SLIDER_FIELDS
        return context


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    """Edit an existing entry."""
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'entries/entry_form.html'

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider_fields'] = SLIDER_FIELDS
        return context


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    """Delete an entry."""
    model = JournalEntry
    template_name = 'entries/entry_confirm_delete.html'
    success_url = reverse_lazy('entry_list')

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)


@login_required
def summary(request):
    """Summary page with trends over time."""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    metric = request.GET.get('metric', 'overall_day_rating')

    # Default to last 30 days
    if not end_date:
        end_date = date.today()
    else:
        end_date = date.fromisoformat(end_date)

    if not start_date:
        start_date = end_date - timedelta(days=30)
    else:
        start_date = date.fromisoformat(start_date)

    entries = JournalEntry.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    ).order_by('date')

    dates = [entry.date.isoformat() for entry in entries]
    values = [getattr(entry, metric) or 0 for entry in entries]

    return render(request, 'entries/summary.html', {
        'dates': dates,
        'values': values,
        'metric': metric,
        'metric_label': METRIC_LABELS.get(metric, metric),
        'available_metric_labels': list(METRIC_LABELS.items()),
        'start_date': start_date,
        'end_date': end_date,
    })
