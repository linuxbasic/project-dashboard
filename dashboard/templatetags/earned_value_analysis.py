from django import template
from datetime import timedelta
from dashboard.chart_utils import get_dates_of_measurement, to_json_array, DAYS_BETWEEN_MEASUREMENTS

register = template.Library()

date_template = 'new Date("{}")'

timedelta_between_measurements = timedelta(days=DAYS_BETWEEN_MEASUREMENTS)


@register.simple_tag
def get_table(project):
    analysis_dates = get_dates_of_measurement(project.start_date, project.get_end_date())
    today = project.today()
    rows = []
    for analysis_date in analysis_dates:
        planned_cost = project.get_planned_cost(analysis_date)
        actual_cost = project.get_cost(analysis_date)
        earned_value = project.get_earnings(analysis_date)
        row = [date_template.format(analysis_date), str(planned_cost),
               str(actual_cost) if analysis_date <= today else None,
               str(actual_cost) if analysis_date + timedelta_between_measurements > today else None,
               str(earned_value) if analysis_date <= today else None]

        rows.append(row)

    return to_json_array(rows)
