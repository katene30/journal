from django import template

register = template.Library()

@register.filter
def truncate_log(value, max_length=94):
    if len(value) > max_length:
        return value[:max_length] + '...'
    return value
