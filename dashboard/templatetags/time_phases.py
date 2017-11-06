from django import template

register = template.Library()


@register.simple_tag
def delta_in_days(phase):
    planned_end_date = phase.get_planned_end_date()
    actual_end_date = phase.get_end_date()
    delta = actual_end_date - planned_end_date
    return delta.days
