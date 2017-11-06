from django.db import models


class Issue(models.Model):
    SEVERITY_CHOICES = ((1, 'Low'), (2, 'High'), (3, 'Very High'),)

    project = models.ForeignKey(to='project.Project', related_name='issues', related_query_name='issue', )
    name = models.CharField(verbose_name='Name', max_length=50, )
    date = models.DateField(verbose_name='Discovery Date', )
    severity = models.PositiveIntegerField(verbose_name='Severity of the Risk', choices=SEVERITY_CHOICES)
    counter_measurement = models.TextField(verbose_name='Counter Measurement', )

    def __str__(self):
        return self.name
