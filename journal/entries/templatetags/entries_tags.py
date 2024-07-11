from django import template

from entries.models import JournalEntry

register = template.Library()


@register.inclusion_tag('entries/entry_list.html', takes_context=True)
def entries(context):
    entries = JournalEntry.objects.order_by('date')
    return {
        'entries': entries,
        'request': context['request'],
    }