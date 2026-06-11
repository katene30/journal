from django import template

from entries.models import JournalEntryPage

register = template.Library()


@register.inclusion_tag('entries/entry_list.html', takes_context=True)
def entries(context):
    entries = JournalEntryPage.objects.live().order_by('-date')
    return {
        'entries': entries,
        'request': context['request'],
    }
