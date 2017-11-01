from django.test import TestCase
from project.tests.utils import create_phase, create_task, create_project
from datetime import timedelta, date


class PhaseStartDateTests(TestCase):
    def test_should_return_project_start_date_if_root_phase(self):
        START_DATE = date(2017, 10, 25)
        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)
        self.assertEqual(phase.get_start_date(), START_DATE)
        self.assertEqual(phase.get_planned_start_date(), START_DATE)

    def test_should_return_planned_start_date(self):
        START_DATE = date(2017, 10, 25)
        TASK_DURATION = 2
        project = create_project(start_date=START_DATE)
        phase1 = create_phase(project=project)
        create_task(phase=phase1, planned_duration=TASK_DURATION)
        phase2 = create_phase(project=project, predecessor=phase1)
        self.assertEqual(phase2.get_start_date(), START_DATE + timedelta(days=TASK_DURATION))

    def test_should_return_planned_start_date_if_no_duration_predictions_available(self):
        START_DATE = date(2017, 10, 25)
        PLANNED_DURATION = 2
        project = create_project(start_date=START_DATE)
        phase1 = create_phase(project=project)
        create_task(phase=phase1, planned_duration=PLANNED_DURATION)
        phase2 = create_phase(project=project, predecessor=phase1)
        self.assertEqual(phase2.get_start_date(), START_DATE + timedelta(days=PLANNED_DURATION))

    def test_should_return_predicted_start_date(self):
        START_DATE = date(2017, 10, 25)
        PLANNED_DURATION = 2
        PREDICTED_DURATION = 4
        project = create_project(start_date=START_DATE)
        phase1 = create_phase(project=project)
        task = create_task(phase=phase1, planned_duration=PLANNED_DURATION)
        phase2 = create_phase(project=project, predecessor=phase1)
        task.duration_predictions.create(date=START_DATE, duration=PREDICTED_DURATION)
        self.assertEqual(phase2.get_start_date(), START_DATE + timedelta(days=PREDICTED_DURATION))

    def test_should_return_predicted_start_date_on_specific_date(self):
        START_DATE = date(2017, 10, 25)
        PLANNED_DURATION = 2
        PREDICTED_DURATION_1 = 3
        PREDICTED_DURATION_2 = 2
        project = create_project(start_date=START_DATE)
        phase1 = create_phase(project=project)
        task = create_task(phase=phase1, planned_duration=PLANNED_DURATION)
        phase2 = create_phase(project=project, predecessor=phase1)

        task.duration_predictions.create(date=date.today() + timedelta(days=1), duration=PREDICTED_DURATION_1)
        task.duration_predictions.create(date=date.today() + timedelta(days=3), duration=PREDICTED_DURATION_2)

        self.assertEqual(phase2.get_start_date(date.today() + timedelta(days=1)),
                         START_DATE + timedelta(days=PREDICTED_DURATION_1))
        self.assertEqual(phase2.get_start_date(date.today() + timedelta(days=2)),
                         START_DATE + timedelta(days=PREDICTED_DURATION_1))
        self.assertEqual(phase2.get_start_date(date.today() + timedelta(days=3)),
                         START_DATE + timedelta(days=PREDICTED_DURATION_2))
        self.assertEqual(phase2.get_start_date(date.today() + timedelta(days=4)),
                         START_DATE + timedelta(days=PREDICTED_DURATION_2))
