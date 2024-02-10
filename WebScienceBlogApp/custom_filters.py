# Create a templatetags directory in your app if not already present
# Inside templatetags, create a new file, e.g., custom_filters.py

# custom_filters.py
from django import template
import random

register = template.Library()

@register.filter(name='random')
def random_element(iterable):
    try:
        return random.choice(iterable)
    except IndexError:
        return None
