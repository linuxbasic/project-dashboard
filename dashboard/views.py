from django.shortcuts import render
from project.models import Project
from datetime import date


def calculate_time_status(project):
    planned_duration = project.get_planned_duration()
    duration = project.get_duration()
    delta = planned_duration - duration
    if delta >= 0:
        return 1
    missmatch = abs((planned_duration / duration) - 1)
    if missmatch <= 0.05:
        return 2
    return 3


def calculate_budget_status(project, date):
    planned_cost = project.get_planned_cost(date)
    actual_cost = project.get_cost(date)
    delta = planned_cost - actual_cost
    if delta >= 0:
        return 1
    missmatch = abs((planned_cost / actual_cost) - 1)
    if missmatch <= 0.05:
        return 2
    return 3


def calculate_scope_status(project, date):
    risk = project.get_unresolved_risk(on_date=date)
    if risk < 3:
        return 1
    if risk == 3:
        return 2
    return 3


def index(request):
    project = Project.objects.all().prefetch_related('phases__tasks__duration_predictions').prefetch_related(
        'phases__tasks__resources').last()
    today = project.today()
    planned_cost = project.get_planned_cost(today)
    actual_cost = project.get_cost(today)
    earned_value = project.get_earnings(today)
    context = {
        'project': project,
        'cost': {
            'planned': planned_cost,
            'actual': actual_cost,
            'earning': earned_value,
            'variance': earned_value - actual_cost,
            'cpi': earned_value / actual_cost,
        },
        'status': {
            'time': calculate_time_status(project),
            'budget': calculate_budget_status(project, today),
            'scope': calculate_scope_status(project, today),
        }
    }

    return render(request=request, template_name='dashboard/dashboard.html', context=context)
