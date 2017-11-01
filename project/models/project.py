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
        return sum([phase.get_planned_duration() for phase in self.phases.all()])

    def get_duration(self):
        return sum([phase.get_duration() for phase in self.phases.all()])

    def get_planned_end_date(self):
        return self.start_date + timedelta(days=self.get_planned_duration())

    def get_end_date(self):
        return self.start_date + timedelta(days=self.get_duration())

    def get_time_status(self):
        planned_duration = self.get_planned_duration()
        duration = self.get_duration()
        return calculate_time_status(planned_duration, duration)

    def get_planned_cost(self):
        return sum([phase.get_planned_cost() for phase in self.phases.all()])

    def get_cost(self, on_date=None):
        return sum([phase.get_cost(on_date) for phase in self.phases.all()])

    def __str__(self):
        return self.name
