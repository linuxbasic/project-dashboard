from datetime import date, timedelta

from django.test import TestCase

from core.shared.test_utils import create_task


class TaskDurationTests(TestCase):
    def test_should_return_planned_duration(self):
        PLANNED_DURATION = 5
        task = create_task(planned_duration=PLANNED_DURATION)
        self.assertEqual(task.get_planned_duration(), PLANNED_DURATION)

    def test_should_return_planned_duration_if_real_not_available(self):
        PLANNED_DURATION = 5
        task = create_task(planned_duration=PLANNED_DURATION)
        self.assertEqual(task.get_duration(), PLANNED_DURATION)

    def test_should_return_predicted_duration_if_available(self):
        PLANNED_DURATION = 1
        PREDICTED_DURATION = 5
        task = create_task(planned_duration=PLANNED_DURATION)
        task.duration_predictions.create(date=date.today() + timedelta(days=2), duration=PREDICTED_DURATION)
        self.assertEqual(task.get_duration(), PREDICTED_DURATION)

    def test_should_return_predicted_duration_on_specific_date(self):
        PLANNED_DURATION = 5
        PREDICTED_DURATION_1 = 3
        PREDICTED_DURATION_2 = 2

        task = create_task(planned_duration=PLANNED_DURATION)
        task.duration_predictions.create(date=date.today() + timedelta(days=1), duration=PREDICTED_DURATION_1)
        task.duration_predictions.create(date=date.today() + timedelta(days=3), duration=PREDICTED_DURATION_2)

        self.assertEqual(task.get_duration(date.today() + timedelta(days=1)), PREDICTED_DURATION_1)
        self.assertEqual(task.get_duration(date.today() + timedelta(days=2)), PREDICTED_DURATION_1)
        self.assertEqual(task.get_duration(date.today() + timedelta(days=3)), PREDICTED_DURATION_2)
        self.assertEqual(task.get_duration(date.today() + timedelta(days=4)), PREDICTED_DURATION_2)