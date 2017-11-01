from django.db import models
from datetime import timedelta


def calculate_time_status(planned_duration, duration):
    delta = planned_duration - duration
    if delta >= 0:
        return 1
    missmatch = abs(planned_duration / duration - 1)
    if missmatch <= 0.05:
        return 2
    return 3


# Create your models here.
class Project(models.Model):
    name = models.CharField(verbose_name='Project Name', max_length=50, )
    start_date = models.DateField(verbose_name='Start Date', )

    def get_planned_duration(self):
        phase_durations = map(lambda phase: phase.get_planned_duration(), self.phases.all())
        return sum(phase_durations)

    def get_real_duration(self):
        phase_durations = map(lambda phase: phase.get_real_duration(), self.phases.all())
        if phase_durations:
            return sum(phase_durations)

    def get_duration(self):
        phase_durations = map(lambda phase: phase.get_duration(), self.phases.all())
        if phase_durations:
            return sum(phase_durations)

    def get_planned_end_date(self):
        return self.start_date + timedelta(days=self.get_planned_duration())

    def get_end_date(self):
        return self.start_date + timedelta(days=self.get_duration())

    def get_time_status(self):
        planned_duration = self.get_planned_duration()
        duration = self.get_duration()
        return calculate_time_status(planned_duration, duration)

    def __str__(self):
        return self.name
