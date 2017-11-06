from datetime import timedelta, date
from django.db import models
from functools import lru_cache
from .resource import Resource


class Project(models.Model):
    name = models.CharField(verbose_name='Project Name', max_length=50, )
    start_date = models.DateField(verbose_name='Start Date', )

    @lru_cache(maxsize=None)
    def today(self):
        return date(2017, 10, 25)

    @lru_cache(maxsize=None)
    def resources(self):
        return Resource.objects.filter(task__phase__project=self).distinct()

    @lru_cache(maxsize=None)
    def get_planned_duration(self):
        return sum([phase.get_planned_duration() for phase in self.phases.all()])

    @lru_cache(maxsize=None)
    def get_duration(self):
        return sum([phase.get_duration() for phase in self.phases.all()])

    @lru_cache(maxsize=None)
    def get_planned_end_date(self):
        return self.start_date + timedelta(days=self.get_planned_duration())

    @lru_cache(maxsize=None)
    def get_end_date(self):
        return self.start_date + timedelta(days=self.get_duration())

    @lru_cache(maxsize=None)
    def get_planned_cost(self, on_date=None):
        return sum([phase.get_planned_cost(on_date) for phase in self.phases.all()])

    @lru_cache(maxsize=None)
    def get_cost(self, on_date=None):
        return sum([phase.get_cost(on_date) for phase in self.phases.all()])

    @lru_cache(maxsize=None)
    def get_earnings(self, on_date=None):
        query = self.earnings.all()
        if on_date is not None:
            query = query.filter(date__lte=on_date)
        return sum(query.values_list('value', flat=True))

    def __str__(self):
        return self.name
