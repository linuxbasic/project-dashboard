from django.db import models


class Risk(models.Model):
    PROBABILITY_CHOICES = ((1, 'Unlikely'), (2, 'Likely'), (3, 'Very Likely'),)
    SEVERITY_CHOICES = ((1, 'Low'), (2, 'High'), (3, 'Very High'),)

    project = models.ForeignKey(to='project.Project', related_name='risks', related_query_name='risk', )
    name = models.CharField(verbose_name='Name', max_length=50, )
    date = models.DateField(verbose_name='Discovery Date', )
    probability = models.PositiveIntegerField(verbose_name='Probability of the Risk', choices=PROBABILITY_CHOICES)
    severity = models.PositiveIntegerField(verbose_name='Severity of the Risk', choices=SEVERITY_CHOICES)
    counter_measurement = models.TextField(verbose_name='Counter Measurement', )

    def __str__(self):
        return self.name
