from datetime import timedelta

DAYS_BETWEEN_MEASUREMENTS = 1


def get_dates_of_measurement(start_date, end_date):
    delta = end_date - start_date

    return [start_date + timedelta(days=i) for i in range(0, delta.days + 1, DAYS_BETWEEN_MEASUREMENTS)]


def to_json_array(array):
    if type(array[0]) is list:
        array = [to_json_array(element) for element in array]
    return '[{}]'.format(','.join([element if element else 'null' for element in array]))
