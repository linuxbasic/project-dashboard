from datetime import timedelta
from django.db import models


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

    def get_planned_cost(self, on_date=None):
        return sum([phase.get_planned_cost(on_date) for phase in self.phases.all()])

    def get_cost(self, on_date=None):
        return sum([phase.get_cost(on_date) for phase in self.phases.all()])

    def __str__(self):
        return self.name
