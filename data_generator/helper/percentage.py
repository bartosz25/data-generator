from math import ceil


def calculate_value(total, percentage):
    return int(ceil(total * percentage / 100))
