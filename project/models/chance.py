from django.db import models


class Chance(models.Model):
    COST_CHOICES = ((1, 'Low'), (2, 'High'), (3, 'Very High'),)
    IMPACT_CHOICES = ((1, 'Small'), (2, 'Big'), (3, 'Very Big'),)

    project = models.ForeignKey(to='project.Project', related_name='chances', related_query_name='chance', )
    name = models.CharField(verbose_name='Name', max_length=50, )
    date = models.DateField(verbose_name='Discovery Date', )
    cost = models.PositiveIntegerField(verbose_name='Cost of the Chance', choices=COST_CHOICES)
    impact = models.PositiveIntegerField(verbose_name='Impact of the Chance', choices=IMPACT_CHOICES)
    used = models.BooleanField(verbose_name='Chance used', default=False)

    def __str__(self):
        return self.name
