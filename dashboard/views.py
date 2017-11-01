from django.shortcuts import render
from project.models import Project
from datetime import date


# Create your views here.


def index(request):
    project = Project.objects.all().prefetch_related('phases__tasks__duration_predictions').prefetch_related(
        'phases__tasks__resources').last()
    context = {'project': project, 'today': date.today()}

    return render(request=request, template_name='dashboard/dashboard.html', context=context)
