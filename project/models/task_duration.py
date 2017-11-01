from django.db import models


class TaskDuration(models.Model):
    task = models.ForeignKey(to='project.Task', related_name='duration_predictions',
                             related_query_name='duration_prediction', )
    date = models.DateField(verbose_name='Day of prediction', auto_created=True)
    duration = models.PositiveIntegerField(verbose_name='Duration of the Task in days', null=True, blank=True, )
