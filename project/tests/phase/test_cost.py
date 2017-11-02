from django.test import TestCase
from core.shared.test_utils import create_project, create_phase, create_task
from datetime import timedelta, date


class PhaseCostTests(TestCase):
    def test_should_return_planned_cost(self):
        START_DATE = date(2017, 10, 25)
        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)

        PLANNED_DURATION_1 = 5
        RESOURCE_COST_1_1 = 50
        RESOURCE_COST_1_2 = 200
        task_1 = create_task(planned_duration=PLANNED_DURATION_1, phase=phase)
        task_1.resources.create(name='resource 1', cost=RESOURCE_COST_1_1)
        task_1.resources.create(name='resource 2', cost=RESOURCE_COST_1_2)
        task_1_cost = PLANNED_DURATION_1 * (RESOURCE_COST_1_1 + RESOURCE_COST_1_2)

        PLANNED_DURATION_2 = 5
        RESOURCE_COST_2_1 = 50
        RESOURCE_COST_2_2 = 200
        task_2 = create_task(planned_duration=PLANNED_DURATION_2, phase=phase, predecessor=task_1)
        task_2.resources.create(name='resource 1', cost=RESOURCE_COST_2_1)
        task_2.resources.create(name='resource 2', cost=RESOURCE_COST_2_2)
        task_2_cost = PLANNED_DURATION_2 * (RESOURCE_COST_2_1 + RESOURCE_COST_2_2)

        self.assertEqual(phase.get_planned_cost(), task_1_cost + task_2_cost)
        self.assertEqual(phase.get_cost(), task_1_cost + task_2_cost)

    def test_should_return_predicted_cost(self):
        START_DATE = date(2017, 10, 25)
        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)

        PLANNED_DURATION_1 = 5
        PREDICTED_DURATION_1 = 3
        RESOURCE_COST_1_1 = 50
        RESOURCE_COST_1_2 = 200
        task_1 = create_task(planned_duration=PLANNED_DURATION_1, phase=phase)
        task_1.resources.create(name='resource 1', cost=RESOURCE_COST_1_1)
        task_1.resources.create(name='resource 2', cost=RESOURCE_COST_1_2)
        task_1.duration_predictions.create(date=START_DATE, duration=PREDICTED_DURATION_1)
        task_1_planned_cost = PLANNED_DURATION_1 * (RESOURCE_COST_1_1 + RESOURCE_COST_1_2)
        task_1_predicted_cost = PREDICTED_DURATION_1 * (RESOURCE_COST_1_1 + RESOURCE_COST_1_2)

        PLANNED_DURATION_2 = 5
        PREDICTED_DURATION_2 = 8
        RESOURCE_COST_2_1 = 50
        RESOURCE_COST_2_2 = 200
        task_2 = create_task(planned_duration=PLANNED_DURATION_2, phase=phase, predecessor=task_1)
        task_2.resources.create(name='resource 1', cost=RESOURCE_COST_2_1)
        task_2.resources.create(name='resource 2', cost=RESOURCE_COST_2_2)
        task_2.duration_predictions.create(date=START_DATE, duration=PREDICTED_DURATION_2)
        task_2_predicted_cost = PREDICTED_DURATION_2 * (RESOURCE_COST_2_1 + RESOURCE_COST_2_2)
        task_2_planned_cost = PLANNED_DURATION_2 * (RESOURCE_COST_2_1 + RESOURCE_COST_2_2)

        self.assertEqual(phase.get_cost(), task_1_predicted_cost + task_2_predicted_cost)
        self.assertEqual(phase.get_planned_cost(), task_1_planned_cost + task_2_planned_cost)
