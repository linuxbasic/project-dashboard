from django.test import TestCase
from core.shared.test_utils import create_project, create_phase, create_task
from datetime import timedelta, date


class TaskStartDateTests(TestCase):
    def test_should_return_phase_start_date_if_root_task(self):
        START_DATE = date(2017, 10, 25)
        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)
        task = create_task(phase=phase)
        self.assertEqual(task.get_start_date(), START_DATE)
        self.assertEqual(task.get_planned_start_date(), START_DATE)

    def test_should_return_planned_start_date(self):
        START_DATE = date(2017, 10, 25)
        TASK_DURATION = 2
        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)
        task_1 = phase.tasks.create(planned_duration=TASK_DURATION)
        task_2 = phase.tasks.create(planned_duration=TASK_DURATION, predecessor=task_1)
        self.assertEqual(task_2.get_start_date(), START_DATE + timedelta(days=TASK_DURATION))
        self.assertEqual(task_2.get_planned_start_date(), START_DATE + timedelta(days=TASK_DURATION))

    def test_should_return_planned_start_date_if_no_duration_predictions_available(self):
        START_DATE = date(2017, 10, 25)
        PLANNED_DURATION = 2
        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)
        task_1 = create_task(phase=phase, planned_duration=PLANNED_DURATION)
        task_2 = create_task(phase=phase, planned_duration=PLANNED_DURATION, predecessor=task_1)
        self.assertEqual(task_2.get_start_date(), START_DATE + timedelta(days=PLANNED_DURATION))

    def test_should_return_predicted_start_date(self):
        START_DATE = date(2017, 10, 25)
        PLANNED_DURATION = 2
        PREDICTED_DURATION = 4
        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)
        task_1 = create_task(phase=phase, planned_duration=PLANNED_DURATION)
        task_1.duration_predictions.create(date=START_DATE, duration=PREDICTED_DURATION)
        task_2 = create_task(phase=phase, planned_duration=PLANNED_DURATION, predecessor=task_1)
        self.assertEqual(task_2.get_start_date(), START_DATE + timedelta(days=PREDICTED_DURATION))

    def test_should_return_predicted_start_date_on_specific_date(self):
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
        task_2 = create_task(phase=phase, planned_duration=PLANNED_DURATION, predecessor=task_1)

        task_1.duration_predictions.create(date=START_DATE_PLUS_1, duration=PREDICTED_DURATION_1)
        task_1.duration_predictions.create(date=START_DATE_PLUS_3, duration=PREDICTED_DURATION_2)

        PREDICTED_END_DATE_1 = START_DATE + timedelta(days=PREDICTED_DURATION_1)
        PREDICTED_END_DATE_2 = START_DATE + timedelta(days=PREDICTED_DURATION_2)

        self.assertEqual(task_2.get_start_date(START_DATE_PLUS_1), PREDICTED_END_DATE_1)
        self.assertEqual(task_2.get_start_date(START_DATE_PLUS_2), PREDICTED_END_DATE_1)
        self.assertEqual(task_2.get_start_date(START_DATE_PLUS_3), PREDICTED_END_DATE_2)
        self.assertEqual(task_2.get_start_date(START_DATE_PLUS_4), PREDICTED_END_DATE_2)
