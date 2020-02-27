from itertools import product
from payment_options.constants import (
    COUNTRIES,
    CURRENCIES,
    PAYMENT_METHODS,
)


def get_combinations():
    return list(product(COUNTRIES, CURRENCIES, PAYMENT_METHODS))


def split_list(condition_list, number):
    for i in range(0, len(condition_list), number):
        yield condition_list[i:i+number]
