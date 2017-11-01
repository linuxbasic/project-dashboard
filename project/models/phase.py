from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from datetime import timedelta


# Create your models here.
class Phase(MPTTModel):
    name = models.CharField(verbose_name='Phase Name', max_length=50, )
    project = models.ForeignKey(to='project.Project', related_name='phases', related_query_name='phase', )
    predecessor = TreeForeignKey(to='self', related_name='successors', related_query_name='successor', null=True,
                                 blank=True, db_index=True)

    def get_planned_duration(self):
        return sum([task.get_planned_duration() for task in self.tasks.all()])

    def get_duration(self):
        return sum([task.get_duration() for task in self.tasks.all()])

    def get_planned_start_date(self):
        if not self.predecessor:
            return self.project.start_date

        predecessor_start_date = self.predecessor.get_planned_start_date()
        predecessor_duration = self.predecessor.get_planned_duration()
        return predecessor_start_date + timedelta(days=predecessor_duration)

    def get_start_date(self):
        if not self.predecessor:
            return self.project.start_date

        predecessor_duration = self.predecessor.get_duration()
        if predecessor_duration:
            predecessor_start_date = self.predecessor.get_start_date()
            return predecessor_start_date + timedelta(days=predecessor_duration)
        return self.get_planned_start_date()

    class MPTTMeta:
        parent_attr = 'predecessor'
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
