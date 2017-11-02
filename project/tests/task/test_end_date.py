from django.test import TestCase
from core.shared.test_utils import create_project, create_phase, create_task
from datetime import timedelta, date


class TaskEndDateTests(TestCase):
    def test_should_return_planned_end_date(self):
        START_DATE = date(2017, 10, 25)
        TASK_DURATION = 2
        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)
        task = create_task(phase=phase, planned_duration=TASK_DURATION)
        self.assertEqual(task.get_planned_end_date(), START_DATE + timedelta(days=TASK_DURATION))
        self.assertEqual(task.get_end_date(), START_DATE + timedelta(days=TASK_DURATION))

    def test_should_return_predicted_end_date(self):
        START_DATE = date(2017, 10, 25)
        PLANNED_DURATION = 2
        PREDICTED_DURATION = 4
        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)
        task = create_task(phase=phase, planned_duration=PLANNED_DURATION)
        task.duration_predictions.create(date=START_DATE, duration=PREDICTED_DURATION)
        self.assertEqual(task.get_end_date(), START_DATE + timedelta(days=PREDICTED_DURATION))

    def test_should_return_predicted_start_date_on_specific_date(self):
        START_DATE = date(2017, 10, 25)
        PLANNED_DURATION = 2
        PREDICTED_DURATION_1 = 3
        PREDICTED_DURATION_2 = 2
        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)
        task = create_task(phase=phase, planned_duration=PLANNED_DURATION)

        task.duration_predictions.create(date=START_DATE + timedelta(days=1), duration=PREDICTED_DURATION_1)
        task.duration_predictions.create(date=START_DATE + timedelta(days=3), duration=PREDICTED_DURATION_2)

        self.assertEqual(task.get_end_date(START_DATE + timedelta(days=1)),
                         START_DATE + timedelta(days=PREDICTED_DURATION_1))
        self.assertEqual(task.get_end_date(START_DATE + timedelta(days=2)),
                         START_DATE + timedelta(days=PREDICTED_DURATION_1))
        self.assertEqual(task.get_end_date(START_DATE + timedelta(days=3)),
                         START_DATE + timedelta(days=PREDICTED_DURATION_2))
        self.assertEqual(task.get_end_date(START_DATE + timedelta(days=4)),
                         START_DATE + timedelta(days=PREDICTED_DURATION_2))

    def test_should_return_predicted_start_date_on_specific_date_for_multile_tasks(self):
        START_DATE = date(2017, 10, 25)
        START_DATE_PLUS_1 = START_DATE + timedelta(days=1)
        START_DATE_PLUS_2 = START_DATE + timedelta(days=2)
        START_DATE_PLUS_3 = START_DATE + timedelta(days=3)
        START_DATE_PLUS_4 = START_DATE + timedelta(days=4)
        PLANNED_DURATION = 2
        PREDICTED_DURATION_1 = 3
        PREDICTED_DURATION_2 = 2
        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)

        task_1 = create_task(phase=phase, planned_duration=PLANNED_DURATION)
        task_1.duration_predictions.create(date=START_DATE_PLUS_1, duration=PREDICTED_DURATION_1)
        task_1.duration_predictions.create(date=START_DATE_PLUS_3, duration=PREDICTED_DURATION_2)

        task_2 = create_task(phase=phase, planned_duration=PLANNED_DURATION, predecessor=task_1)
        task_2.duration_predictions.create(date=START_DATE_PLUS_1, duration=PREDICTED_DURATION_1)
        task_2.duration_predictions.create(date=START_DATE_PLUS_3, duration=PREDICTED_DURATION_2)

        PREDICTED_END_DATE_1 = START_DATE + timedelta(days=(2 * PREDICTED_DURATION_1))
        PREDICTED_END_DATE_2 = START_DATE + timedelta(days=(2 * PREDICTED_DURATION_2))

        self.assertEqual(task_2.get_end_date(START_DATE_PLUS_1), PREDICTED_END_DATE_1)
        self.assertEqual(task_2.get_end_date(START_DATE_PLUS_2), PREDICTED_END_DATE_1)
        self.assertEqual(task_2.get_end_date(START_DATE_PLUS_3), PREDICTED_END_DATE_2)
        self.assertEqual(task_2.get_end_date(START_DATE_PLUS_4), PREDICTED_END_DATE_2)
