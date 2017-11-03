from django.test import TestCase
from core.shared.test_utils import create_project, create_phase, create_task
from datetime import timedelta, date


class ProjectEarningTests(TestCase):
    def test_should_return_earning(self):
        START_DATE = date(2017, 10, 25)
        EARNING = 500
        project = create_project(start_date=START_DATE)

        project.earnings.create(name='Earning', date=START_DATE, value=EARNING)

        self.assertEqual(project.get_earnings(), EARNING)

    def test_should_return_combined_earnings(self):
        START_DATE = date(2017, 10, 25)
        START_DATE_PLUS_1 = START_DATE + timedelta(days=1)
        START_DATE_PLUS_2 = START_DATE + timedelta(days=2)
        START_DATE_PLUS_3 = START_DATE + timedelta(days=3)
        START_DATE_PLUS_4 = START_DATE + timedelta(days=4)
        EARNING_1 = 500
        EARNING_2 = 1000
        project = create_project(start_date=START_DATE)

        project.earnings.create(name='Earning 1', date=START_DATE_PLUS_1, value=EARNING_1)
        project.earnings.create(name='Earning 1', date=START_DATE_PLUS_3, value=EARNING_2)

        self.assertEqual(project.get_earnings(START_DATE), 0)
        self.assertEqual(project.get_earnings(START_DATE_PLUS_1), EARNING_1)
        self.assertEqual(project.get_earnings(START_DATE_PLUS_2), EARNING_1)
        self.assertEqual(project.get_earnings(START_DATE_PLUS_3), EARNING_1 + EARNING_2)
        self.assertEqual(project.get_earnings(START_DATE_PLUS_4), EARNING_1 + EARNING_2)
