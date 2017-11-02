from datetime import date, timedelta

from django.test import TestCase

from core.shared.test_utils import create_task, create_project, create_phase


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
        START_DATE = date(2017, 10, 25)
        PLANNED_DURATION = 5
        PREDICTED_DURATION = 3
        RESOURCE_COST_1 = 50
        RESOURCE_COST_2 = 200
        task = create_task(planned_duration=PLANNED_DURATION)
        task.resources.create(name='resource 1', cost=RESOURCE_COST_1)
        task.resources.create(name='resource 2', cost=RESOURCE_COST_2)
        task.duration_predictions.create(date=START_DATE + timedelta(days=2), duration=PREDICTED_DURATION)

        self.assertEqual(task.get_cost(), PREDICTED_DURATION * (RESOURCE_COST_1 + RESOURCE_COST_2))
        self.assertEqual(task.get_planned_cost(), PLANNED_DURATION * (RESOURCE_COST_1 + RESOURCE_COST_2))

    def test_should_return_correct_cost_on_specific_date(self):
        START_DATE = date(2017, 10, 25)
        START_DATE_PLUS_1 = START_DATE + timedelta(days=1)
        START_DATE_PLUS_2 = START_DATE + timedelta(days=2)
        START_DATE_PLUS_3 = START_DATE + timedelta(days=3)
        START_DATE_PLUS_4 = START_DATE + timedelta(days=4)
        PLANNED_DURATION = 3
        RESOURCE_COST_1 = 50
        RESOURCE_COST_2 = 200

        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)
        task = create_task(planned_duration=PLANNED_DURATION, phase=phase)
        task.resources.create(name='resource 1', cost=RESOURCE_COST_1)
        task.resources.create(name='resource 2', cost=RESOURCE_COST_2)

        PLANNED_COST = PLANNED_DURATION * (RESOURCE_COST_1 + RESOURCE_COST_2)

        self.assertEqual(task.get_cost(START_DATE), 0)
        self.assertEqual(task.get_cost(START_DATE_PLUS_1), PLANNED_COST * (1 / 3))
        self.assertEqual(task.get_cost(START_DATE_PLUS_2), PLANNED_COST * (2 / 3))
        self.assertEqual(task.get_cost(START_DATE_PLUS_3), PLANNED_COST)
        self.assertEqual(task.get_cost(START_DATE_PLUS_4), PLANNED_COST)

        self.assertEqual(task.get_planned_cost(START_DATE), 0)
        self.assertEqual(task.get_planned_cost(START_DATE_PLUS_1), PLANNED_COST * (1 / 3))
        self.assertEqual(task.get_planned_cost(START_DATE_PLUS_2), PLANNED_COST * (2 / 3))
        self.assertEqual(task.get_planned_cost(START_DATE_PLUS_3), PLANNED_COST)
        self.assertEqual(task.get_planned_cost(START_DATE_PLUS_4), PLANNED_COST)

    def test_should_return_correct_cost_on_specific_date_with_predictions(self):
        START_DATE = date(2017, 10, 25)

        def start_date_plus(days):
            return START_DATE + timedelta(days=days)

        PLANNED_DURATION = 4
        PREDICTED_DURATION_TASK_1 = 3
        PREDICTED_DURATION_TASK_2 = 2
        RESOURCE_COST_TASK_1 = 50
        RESOURCE_COST_TASK_2 = 200

        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)
        task_1 = create_task(phase=phase, planned_duration=PLANNED_DURATION)

        task_1.duration_predictions.create(date=start_date_plus(1), duration=PREDICTED_DURATION_TASK_1)
        task_1.resources.create(name='resource 1', cost=RESOURCE_COST_TASK_1)

        task_2 = create_task(phase=phase, planned_duration=PLANNED_DURATION, predecessor=task_1)
        task_2.duration_predictions.create(date=start_date_plus(3), duration=PREDICTED_DURATION_TASK_2)
        task_2.resources.create(name='resource 2', cost=RESOURCE_COST_TASK_2)

        self.assertEqual(task_1.get_cost(START_DATE), 0)
        self.assertEqual(task_1.get_cost(start_date_plus(1)), 1 * RESOURCE_COST_TASK_1)
        self.assertEqual(task_1.get_cost(start_date_plus(2)), 2 * RESOURCE_COST_TASK_1)
        self.assertEqual(task_1.get_cost(start_date_plus(3)), 3 * RESOURCE_COST_TASK_1)
        self.assertEqual(task_1.get_cost(start_date_plus(4)), 3 * RESOURCE_COST_TASK_1)

        self.assertEqual(task_1.get_planned_cost(START_DATE), 0)
        self.assertEqual(task_1.get_planned_cost(start_date_plus(1)), 1 * RESOURCE_COST_TASK_1)
        self.assertEqual(task_1.get_planned_cost(start_date_plus(2)), 2 * RESOURCE_COST_TASK_1)
        self.assertEqual(task_1.get_planned_cost(start_date_plus(3)), 3 * RESOURCE_COST_TASK_1)
        self.assertEqual(task_1.get_planned_cost(start_date_plus(4)), 4 * RESOURCE_COST_TASK_1)
        self.assertEqual(task_1.get_planned_cost(start_date_plus(5)), 4 * RESOURCE_COST_TASK_1)

        self.assertEqual(task_2.get_cost(START_DATE), 0)
        self.assertEqual(task_2.get_cost(start_date_plus(3)), 0)
        self.assertEqual(task_2.get_cost(start_date_plus(4)), 1 * RESOURCE_COST_TASK_2)
        self.assertEqual(task_2.get_cost(start_date_plus(5)), 2 * RESOURCE_COST_TASK_2)
        self.assertEqual(task_2.get_cost(start_date_plus(6)), 2 * RESOURCE_COST_TASK_2)

        self.assertEqual(task_2.get_planned_cost(START_DATE), 0)
        self.assertEqual(task_2.get_planned_cost(start_date_plus(4)), 0)
        self.assertEqual(task_2.get_planned_cost(start_date_plus(5)), 1 * RESOURCE_COST_TASK_2)
        self.assertEqual(task_2.get_planned_cost(start_date_plus(6)), 2 * RESOURCE_COST_TASK_2)
        self.assertEqual(task_2.get_planned_cost(start_date_plus(7)), 3 * RESOURCE_COST_TASK_2)
        self.assertEqual(task_2.get_planned_cost(start_date_plus(8)), 4 * RESOURCE_COST_TASK_2)
        self.assertEqual(task_2.get_planned_cost(start_date_plus(9)), 4 * RESOURCE_COST_TASK_2)
