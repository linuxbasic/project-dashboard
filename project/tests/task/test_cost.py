from datetime import date, timedelta

from django.test import TestCase

from core.shared.test_utils import create_task


class TaskCostTests(TestCase):
    def test_should_return_planned_cost_of_single_resource(self):
        PLANNED_DURATION = 5
        RESOURCE_COST = 50
        task = create_task(planned_duration=PLANNED_DURATION)
        task.resources.create(name='resource', cost=RESOURCE_COST)

        self.assertEqual(task.get_planned_cost(), PLANNED_DURATION * RESOURCE_COST)

    def test_should_return_planned_cost_of_multiple_resources(self):
        PLANNED_DURATION = 5
        RESOURCE_COST_1 = 50
        RESOURCE_COST_2 = 200
        task = create_task(planned_duration=PLANNED_DURATION)
        task.resources.create(name='resource 1', cost=RESOURCE_COST_1)
        task.resources.create(name='resource 2', cost=RESOURCE_COST_2)

        self.assertEqual(task.get_planned_cost(), PLANNED_DURATION * (RESOURCE_COST_1 + RESOURCE_COST_2))
        self.assertEqual(task.get_cost(), PLANNED_DURATION * (RESOURCE_COST_1 + RESOURCE_COST_2))

    def test_should_return_predicted_cost_of_multiple_resources(self):
        PLANNED_DURATION = 5
        PREDICTED_DURATION = 3
        RESOURCE_COST_1 = 50
        RESOURCE_COST_2 = 200
        task = create_task(planned_duration=PLANNED_DURATION)
        task.resources.create(name='resource 1', cost=RESOURCE_COST_1)
        task.resources.create(name='resource 2', cost=RESOURCE_COST_2)
        task.duration_predictions.create(date=date.today() + timedelta(days=2), duration=PREDICTED_DURATION)

        self.assertEqual(task.get_cost(), PREDICTED_DURATION * (RESOURCE_COST_1 + RESOURCE_COST_2))
        self.assertEqual(task.get_planned_cost(), PLANNED_DURATION * (RESOURCE_COST_1 + RESOURCE_COST_2))
