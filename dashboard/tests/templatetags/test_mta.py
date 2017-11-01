from django.test import TestCase
from datetime import date

# Create your tests here.
from dashboard.templatetags.mta import get_days, get_table
from core.shared.test_utils import create_project, create_phase, create_task


class MTATemplatetagsTests(TestCase):
    def test_should_return_list_of_dates(self):
        START_DATE = date(2017, 10, 1)
        END_DATE = date(2017, 10, 6)
        EXPECED_DATES = [date(2017, 10, 1), date(2017, 10, 2), date(2017, 10, 3), date(2017, 10, 4), date(2017, 10, 5),
                         date(2017, 10, 6), ]

        self.assertListEqual(get_days(START_DATE, END_DATE), EXPECED_DATES)
