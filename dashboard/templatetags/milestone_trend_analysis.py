from django import template
from dashboard.chart_utils import get_days, to_json_array

register = template.Library()

date_template = 'new Date("{}")'


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
