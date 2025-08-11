# website/templatetags/duration_extras.py
from django import template

register = template.Library()

@register.filter
def format_duration(value):
    if not value:
        return ""
    total_minutes = int(value.total_seconds() // 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours == 0:
        return f"{minutes} минут"
    elif minutes == 0:
        return f"{hours} часа"
    else:
        return f"{hours} ч {minutes} мин"
