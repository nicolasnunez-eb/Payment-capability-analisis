from payment_options.constants import (
    COUNTRIES,
    CURRENCIES,
)


class CheckoutSettingIterator():

    def __init__(self):
        self._index_country = 0
        self._index_currency = 0

    def __next__(self):
        try:
            country_currency = (
                COUNTRIES[self._index_country],
                CURRENCIES[self._index_currency]
            )
            self._index_currency += 1
            if self._index_currency == len(CURRENCIES):
                self._index_country += 1
                self._index_currency = 0

            return country_currency
        except IndexError:
            raise StopIteration()


class CheckoutSetting():

    def __iter__(self):
        return CheckoutSettingIterator()
