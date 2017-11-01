from datetime import date

from project.models import Project, Phase, Task, TaskDuration


def create_project(name='task', start_date=date.today()):
    return Project.objects.create(name=name, start_date=start_date)


def create_phase(name='phase', project=None, predecessor=None):
    if project is None:
        project = create_project()
    return Phase.objects.create(name=name, project=project, predecessor=predecessor)


def create_task(name='task', planned_duration=1, phase=None, predecessor=None):
    if phase is None:
        phase = create_phase()
    return Task.objects.create(name=name, phase=phase, planned_duration=planned_duration, predecessor=predecessor)


def create_task_duration(date=date.today(), duration=2, task=None):
    if task is None:
        task = create_task()
    return TaskDuration.objects.create(task=task, date=date, duration=duration)