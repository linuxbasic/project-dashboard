from datetime import timedelta

def get_days(start_date, end_date):
    delta = end_date - start_date

    return [start_date + timedelta(days=i) for i in range(0, delta.days + 1, 7)]


def to_json_array(array):
    if type(array[0]) is list:
        array = [to_json_array(element) for element in array]
    return '[{}]'.format(','.join([element if element else 'null' for element in array]))