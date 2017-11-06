from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from datetime import timedelta
from functools import lru_cache


# Create your models here.
class Phase(MPTTModel):
    name = models.CharField(verbose_name='Phase Name', max_length=50, )
    project = models.ForeignKey(to='project.Project', related_name='phases', related_query_name='phase', )
    predecessor = TreeForeignKey(to='self', related_name='successors', related_query_name='successor', null=True,
                                 blank=True, db_index=True)

    @lru_cache(maxsize=None)
    def get_planned_duration(self):
        return sum([task.get_planned_duration() for task in self.tasks.all()])

    @lru_cache(maxsize=None)
    def get_duration(self, on_date=None):
        return sum([task.get_duration(on_date) for task in self.tasks.all()])

    @lru_cache(maxsize=None)
    def get_planned_start_date(self):
        if not self.predecessor:
            return self.project.start_date

        return self.predecessor.get_planned_end_date()

    @lru_cache(maxsize=None)
    def get_start_date(self, on_date=None):
        if not self.predecessor:
            return self.project.start_date

        return self.predecessor.get_end_date(on_date)

    @lru_cache(maxsize=None)
    def get_planned_end_date(self):
        planned_start_date = self.get_planned_start_date()
        planned_duration = self.get_planned_duration()
        return planned_start_date + timedelta(days=planned_duration)

    @lru_cache(maxsize=None)
    def get_end_date(self, on_date=None):
        start_date = self.get_start_date(on_date)
        duration = self.get_duration(on_date)
        return start_date + timedelta(days=duration)

    @lru_cache(maxsize=None)
    def get_planned_cost(self, on_date=None):
        return sum([task.get_planned_cost(on_date) for task in self.tasks.all()])

    @lru_cache(maxsize=None)
    def get_cost(self, on_date=None):
        return sum([task.get_cost(on_date) for task in self.tasks.all()])

    class MPTTMeta:
        parent_attr = 'predecessor'
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
