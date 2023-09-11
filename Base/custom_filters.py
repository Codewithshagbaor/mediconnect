
from django import template

register = template.Library()

@register.filter
def ends_with(value, arg):
    """Check if the value ends with a specific string."""
    return value.endswith(arg)
