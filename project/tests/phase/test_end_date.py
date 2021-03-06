from django.test import TestCase
from core.shared.test_utils import create_project, create_phase, create_task
from datetime import timedelta, date


class PhaseEndDateTests(TestCase):
    def test_should_return_planned_end_date(self):
        START_DATE = date(2017, 10, 25)
        TASK_DURATION = 2
        project = create_project(start_date=START_DATE)
        phase1 = create_phase(project=project)
        create_task(phase=phase1, planned_duration=TASK_DURATION)
        self.assertEqual(phase1.get_planned_end_date(), START_DATE + timedelta(days=TASK_DURATION))
        self.assertEqual(phase1.get_end_date(), START_DATE + timedelta(days=TASK_DURATION))

    def test_should_return_predicted_end_date(self):
        START_DATE = date(2017, 10, 25)
        PLANNED_DURATION = 2
        PREDICTED_DURATION = 4
        project = create_project(start_date=START_DATE)
        phase1 = create_phase(project=project)
        task = create_task(phase=phase1, planned_duration=PLANNED_DURATION)
        task.duration_predictions.create(date=START_DATE, duration=PREDICTED_DURATION)
        self.assertEqual(phase1.get_end_date(), START_DATE + timedelta(days=PREDICTED_DURATION))

    def test_should_return_predicted_start_date_on_specific_date(self):
        START_DATE = date(2017, 10, 25)
        PLANNED_DURATION = 2
        PREDICTED_DURATION_1 = 3
        PREDICTED_DURATION_2 = 2
        project = create_project(start_date=START_DATE)
        phase1 = create_phase(project=project)
        task = create_task(phase=phase1, planned_duration=PLANNED_DURATION)

        task.duration_predictions.create(date=START_DATE + timedelta(days=1), duration=PREDICTED_DURATION_1)
        task.duration_predictions.create(date=START_DATE + timedelta(days=3), duration=PREDICTED_DURATION_2)

        self.assertEqual(phase1.get_end_date(START_DATE + timedelta(days=1)),
                         START_DATE + timedelta(days=PREDICTED_DURATION_1))
        self.assertEqual(phase1.get_end_date(START_DATE + timedelta(days=2)),
                         START_DATE + timedelta(days=PREDICTED_DURATION_1))
        self.assertEqual(phase1.get_end_date(START_DATE + timedelta(days=3)),
                         START_DATE + timedelta(days=PREDICTED_DURATION_2))
        self.assertEqual(phase1.get_end_date(START_DATE + timedelta(days=4)),
                         START_DATE + timedelta(days=PREDICTED_DURATION_2))
