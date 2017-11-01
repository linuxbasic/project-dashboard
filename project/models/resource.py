from django.db import models


# Create your models here.
class Resource(models.Model):
    name = models.CharField(verbose_name='Task Name', max_length=50, )
    cost = models.PositiveIntegerField(verbose_name='Cost per day/unit')

    def __str__(self):
        return self.name
