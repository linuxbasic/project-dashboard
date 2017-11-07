from django.db import models


class Risk(models.Model):
    PROBABILITY_CHOICES = ((1, 'Low'), (2, 'High'), (3, 'Very High'),)
    SEVERITY_CHOICES = ((1, 'Low'), (2, 'High'), (3, 'Very High'),)
    RISK_MAP = {
        1: 'Very Low',
        2: 'Low',
        3: 'Medium',
        4: 'High',
        6: 'Very High',
        9: 'Extremely High',
    }

    project = models.ForeignKey(to='project.Project', related_name='risks', related_query_name='risk', )
    name = models.CharField(verbose_name='Name', max_length=50, )
    date = models.DateField(verbose_name='Discovery Date', )
    probability = models.PositiveIntegerField(verbose_name='Probability of the Risk', choices=PROBABILITY_CHOICES)
    severity = models.PositiveIntegerField(verbose_name='Severity of the Risk', choices=SEVERITY_CHOICES)
    counter_measurement = models.TextField(verbose_name='Counter Measurement', )
    resolved = models.BooleanField(verbose_name='Risk resolved', default=False)

    def get_risk(self):
        return self.severity * self.probability

    def display_risk(self):
        return self.RISK_MAP.get(self.get_risk())

    def __str__(self):
        return self.name
