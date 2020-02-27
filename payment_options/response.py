import json


class BaseResponse:

    def __init__(self, payment_options):
        self.payment_options = payment_options

    def _sort_dictionary_item(self, dictionary, key):
        for elem in dictionary:
            elem[key].sort()

    def sort_instrument_types(self):
        for payment_option in self.payment_options:
            if payment_option.get('instrument_types'):
                self._sort_dictionary_item(
                        payment_option['instrument_types'],
                        'variants'
                    )

    def to_json(self):
        return json.dumps(
            {'payment_options': self.payment_options},
            indent=4,
            sort_keys=True
        )

    def to_pretty_html_tag(self, html_builder):
        return html_builder.get_html_tag(content=self.to_json(), tag='pre', attributes={'class': 'prettyprint'})


class DiffResponse:

    def __init__(self, diff, has_differences=None):
        self.diff = diff
        self._has_differences = has_differences

    def to_pretty_html_tag(self, html_builder):
        return html_builder.get_html_tag(content=self.diff, tag='pre', attributes={'class': 'prettyprint'})

    def set_has_difference(self, has_differences):
        self._has_differences = has_differences

    @property
    def has_differences(self):
        return self._has_differences
