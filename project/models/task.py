from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from datetime import timedelta


# Create your models here.
class Task(MPTTModel):
    name = models.CharField(verbose_name='Task Name', max_length=50, )
    phase = models.ForeignKey(to='project.Phase', related_name='tasks', related_query_name='task', )
    predecessor = TreeForeignKey(to='self', related_name='successors', related_query_name='successor', null=True,
                                 blank=True, db_index=True)
    resources = models.ManyToManyField('project.Resource', blank=True)

    planned_duration = models.PositiveIntegerField(verbose_name='Planned Duration of the Task in days')

    def get_last_duration_prediction(self, on_date):
        query = self.duration_predictions
        try:
            if on_date:
                query = query.filter(date__lte=on_date)
            return query.latest('date')
        except:
            return None

    def get_planned_duration(self):
        return self.planned_duration

    def get_duration(self, on_date=None):
        last_duration_prediction = self.get_last_duration_prediction(on_date)
        if last_duration_prediction:
            return last_duration_prediction.duration
        return self.get_planned_duration()

    def get_resource_cost(self):
        return sum(self.resources.all().values_list('cost', flat=True))

    def get_planned_cost(self, on_date=None):
        if on_date is None:
            return self.get_planned_duration() * self.get_resource_cost()

        start_date = self.get_planned_start_date()
        if on_date <= start_date:
            return 0

        end_date = self.get_planned_end_date()
        if on_date >= end_date:
            return self.get_planned_cost()

        task_duration = self.get_planned_duration()
        days_spend_on_task = (on_date - start_date).days
        return self.get_planned_cost() * (days_spend_on_task / task_duration)

    def get_cost(self, on_date=None):
        if on_date is None:
            return self.get_duration(on_date) * self.get_resource_cost()

        start_date = self.get_start_date(on_date)
        if on_date <= start_date:
            return 0

        end_date = self.get_end_date(on_date)
        if on_date >= end_date:
            return self.get_cost()

        task_duration = self.get_duration(on_date)
        days_spend_on_task = (on_date - start_date).days
        return self.get_cost() * (days_spend_on_task / task_duration)

    def get_start_date(self, on_date=None):
        if not self.predecessor:
            return self.phase.get_start_date(on_date)
        return self.predecessor.get_end_date(on_date)

    def get_planned_start_date(self):
        if not self.predecessor:
            return self.phase.get_planned_start_date()
        return self.predecessor.get_planned_end_date()

    def get_planned_end_date(self):
        start_date = self.get_planned_start_date()
        duration = self.get_planned_duration()
        return start_date + timedelta(days=duration)

    def get_end_date(self, on_date=None):
        start_date = self.get_start_date(on_date)
        duration = self.get_duration(on_date)
        return start_date + timedelta(days=duration)

    class MPTTMeta:
        parent_attr = 'predecessor'
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
