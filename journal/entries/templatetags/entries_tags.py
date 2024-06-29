from django import template

from journal.entries.models import JournalEntry

register = template.Library()


@register.inclusion_tag('entries/entry_list.html', takes_context=True)
def entries(context):
    return {
        'entries': JournalEntry.objects.all(),
        'request': context['request'],
    }