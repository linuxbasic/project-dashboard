from django import template
from datetime import timedelta

register = template.Library()

date_template = 'new Date("{}")'


def get_days(start_date, end_date):
    delta = end_date - start_date

    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]


def to_json_array(array):
    if type(array[0]) is list:
        array = [to_json_array(element) for element in array]
    return '[{}]'.format(','.join([element if element else 'null' for element in array]))


@register.simple_tag
def get_headers(project):
    return ['Date of Prediction'] + [phase.name for phase in project.phases.all()]


@register.simple_tag
def get_table(project):
    prediction_dates = get_days(project.start_date, project.get_end_date())
    rows = []
    for prediction_date in prediction_dates:
        row = [date_template.format(prediction_date)] + [date_template.format(phase.get_end_date(prediction_date)) for
                                                         phase in project.phases.all()]
        rows.append(row)

    return to_json_array(rows)
