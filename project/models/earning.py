from django.db import models


class Earning(models.Model):
    name = models.CharField(verbose_name='Earning', max_length=50, )
    date = models.DateField(verbose_name='Payment Date', )
    project = models.ForeignKey(to='project.Project', related_name='earnings', related_query_name='earning', )
    value = models.PositiveIntegerField(verbose_name='Earning Value in CHF')

    def __str__(self):
        return self.name
