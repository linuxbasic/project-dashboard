from django.shortcuts import render
from project.models import Project
from datetime import date


# Create your views here.


def index(request):
    context = {'project': Project.objects.all().last(), 'today': date.today()}

    return render(request=request, template_name='dashboard/dashboard.html', context=context)
