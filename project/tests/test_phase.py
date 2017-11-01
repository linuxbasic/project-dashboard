from django.test import TestCase
from .utils import create_phase, create_task, create_project, create_task_duration
from datetime import timedelta, date


class PhaseTests(TestCase):
    def test_should_return_project_start_date_as_planned_start_date_if_root_phase(self):
        START_DATE = date(2017, 10, 25)
        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)
        self.assertEqual(phase.get_planned_start_date(), START_DATE)

    def test_should_return_planned_start_date(self):
        START_DATE = date(2017, 10, 25)
        TASK_DURATION = 2
        project = create_project(start_date=START_DATE)
        phase1 = create_phase(project=project)
        create_task(phase=phase1, planned_duration=TASK_DURATION)
        phase2 = create_phase(project=project, predecessor=phase1)
        self.assertEqual(phase2.get_start_date(), START_DATE + timedelta(days=TASK_DURATION))

    def test_should_return_project_start_date_if_root_phase(self):
        START_DATE = date(2017, 10, 25)
        project = create_project(start_date=START_DATE)
        phase = create_phase(project=project)
        self.assertEqual(phase.get_start_date(), START_DATE)

    def should_return_real_start_date(self):
        START_DATE = date(2017, 10, 25)
        PLANNED_DURATION = 2
        REAL_DURATION = 4
        project = create_project(start_date=START_DATE)
        phase1 = create_phase(project=project)
        task = create_task(phase=phase1, planned_duration=PLANNED_DURATION)
        phase2 = create_phase(project=project, predecessor=phase1)
        create_task_duration(task=task, date=START_DATE, duration=REAL_DURATION)
        self.assertEqual(phase2.get_start_date(), START_DATE + timedelta(days=REAL_DURATION))

    def should_return_planned_start_date_if_no_duration_predictions_available(self):
        START_DATE = date('2017-10-25')
        PLANNED_DURATION = 2
        project = create_project(start_date=START_DATE)
        phase1 = create_phase(project=project)
        task = create_task(phase=phase1, planned_duration=PLANNED_DURATION)
        phase2 = create_phase(project=project, predecessor=phase1)
        self.assertEqual(phase2.get_start_date(), START_DATE + timedelta(days=PLANNED_DURATION))
