from django import template

# chart filters
register = template.Library()

@register.filter
def get_range(value):
    """
    Creates a range from 0 to value-1
    Usage: {% for i in value|get_range %}
    """
    return range(int(value))

@register.filter
def index(sequence, position):
    """
    Returns item at index in sequence
    Usage: {{ sequence|index:position }}
    """
    try:
        return sequence[position]
    except:
        return None