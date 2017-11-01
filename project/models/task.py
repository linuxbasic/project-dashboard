from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


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

    class MPTTMeta:
        parent_attr = 'predecessor'
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
