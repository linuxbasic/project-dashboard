from django.test import TestCase
from project.models import (Project, Phase, Task, Resource)


# Create your tests here.
class Test(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name='Demo Project', start_date='2017-10-25')
        self.resource_1 = Resource.objects.create(name='Resource 1', cost=150)
        self.resource_2 = Resource.objects.create(name='Resource 2', cost=90)
        self.resource_3 = Resource.objects.create(name='Resource 3', cost=200)

        self.phase_1 = Phase.objects.create(name='Phase 1', project=self.project)
        self.task_1_1 = Task.objects.create(name='Task 1.1', phase=self.phase_1, planned_duration=1, )
        self.task_1_1.resources.add(self.resource_3)
        self.task_1_1.duration_predictions.create(date='2017-10-23', duration=2)

        self.phase_2 = Phase.objects.create(name='Phase 2', project=self.project, predecessor=self.phase_1)
        self.task_2_1 = Task.objects.create(name='Task 2.1', phase=self.phase_2, planned_duration=5, )
        self.task_2_1.resources.add(self.resource_3)
        self.task_2_1.resources.add(self.resource_1)
        self.task_2_1.duration_predictions.create(date='2017-10-23', duration=4)
        self.task_2_1.duration_predictions.create(date='2017-10-25', duration=5)
        self.task_2_1.duration_predictions.create(date='2017-10-27', duration=7)
        self.task_2_2 = Task.objects.create(name='Task 2.2', phase=self.phase_2, planned_duration=3,
                                            predecessor=self.task_2_1)
        self.task_2_1.resources.add(self.resource_2)
