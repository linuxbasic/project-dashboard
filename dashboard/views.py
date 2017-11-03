from django.shortcuts import render
from project.models import Project
from datetime import date


def calculate_time_status(project):
    planned_duration = project.get_planned_duration()
    duration = project.get_duration()
    delta = planned_duration - duration
    if delta >= 0:
        return 1
    missmatch = abs(planned_duration / duration - 1)
    if missmatch <= 0.05:
        return 2
    return 3


def index(request):
    project = Project.objects.all().prefetch_related('phases__tasks__duration_predictions').prefetch_related(
        'phases__tasks__resources').last()
    today = date.today()
    context = {
        'project': project,
        'today': today,
        'status': {
            'time': calculate_time_status(project)
        }
    }

    return render(request=request, template_name='dashboard/dashboard.html', context=context)
