from django.core.management.base import BaseCommand
from project.models import (Project, Phase, Task, TaskDuration, Resource)
from datetime import datetime
import random


def create_phases(project, count):
    phases = []
    predecessor = None
    for i in range(count):
        phase = Phase.objects.create(name='Phase {}'.format(i), project=project, predecessor=predecessor)
        predecessor = phase
        phases.append(phase)

    return phases


def create_tasks(phase, count, max_duaration):
    tasks = []
    predecessor = None
    for i in range(count):
        duration = random.randint(1, max_duaration + 1)
        task = Task.objects.create(name='Task {}'.format(i), phase=phase, predecessor=predecessor,
                                   planned_duration=duration)
        predecessor = task
        tasks.append(task)

    return tasks


class Command(BaseCommand):
    def handle(self, *args, **options):
        project = Project.objects.create(name='Demo Project', start_date='2017-10-25')
        resource_1 = Resource.objects.create(name='Resource 1', cost=150)
        resource_2 = Resource.objects.create(name='Resource 2', cost=90)
        resource_3 = Resource.objects.create(name='Resource 3', cost=200)

        phase_1 = Phase.objects.create(name='Phase 1', project=project)
        task_1_1 = Task.objects.create(name='Task 1.1', phase=phase_1, planned_duration=1, )
        task_1_1.resources.add(resource_3)
        task_1_1.duration_predictions.create(date='2017-10-23', duration=2)

        phase_2 = Phase.objects.create(name='Phase 2', project=project, predecessor=phase_1)
        task_2_1 = Task.objects.create(name='Task 2.1', phase=phase_2, planned_duration=5, )
        task_2_1.resources.add(resource_3)
        task_2_1.resources.add(resource_1)
        task_2_1.duration_predictions.create(date='2017-10-23', duration=4)
        task_2_1.duration_predictions.create(date='2017-10-25', duration=5)
        task_2_1.duration_predictions.create(date='2017-10-27', duration=7)
        task_2_2 = Task.objects.create(name='Task 2.2', phase=phase_2, planned_duration=3, predecessor=task_2_1)
        task_2_1.resources.add(resource_2)

        #phase_3 = Phase.objects.create(name='Phase 3', project=project, predecessor=phase_2)
