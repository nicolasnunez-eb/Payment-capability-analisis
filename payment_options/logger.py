from termcolor import colored
import json
from html_writer import Html
from subprocess import PIPE, run

from payment_options.constants import TABLE_HEADERS
from payment_options.response import (
    BaseResponse,
    DiffResponse,
)


class Logger():

    def log_conditions(self, conditions):
        text = colored(json.dumps(conditions), 'yellow')
        print(text)

    def log_response(self, data):
        text = colored(data, 'green')
        print("RESPONSE:")
        print(text)
        print("**********END RESPONSE**********")

    def log_error(self):
        text = colored("Create checkout setting for an organization failed", 'red')
        print(text)


class ResponseManager():

    def __init__(self):
        self.logger = Logger()
        self.html_builder = HtmlBuilder()
        self.conditions = []
        self.order_service_responses = []
        self.pcs_responses = []
        self.responses = []

    def add_conditions(self, conditions):
        self.conditions.append(conditions)
        self.logger.log_conditions(conditions)

    def add_order_service_response(self, data):
        self.order_service_responses.append(BaseResponse(data.get('payment_options')))
        self.logger.log_response(data)

    def add_pcs_response(self, data):
        self.pcs_responses.append(BaseResponse(data.get('payment_options')))
        self.logger.log_response(data)

    def join_responses(self):
        for i in range(len(self.order_service_responses)):
            dict_response = {}
            dict_response['conditions'] = self.conditions[i]
            dict_response['os_response'] = self.order_service_responses[i]
            dict_response['pcs_response'] = self.pcs_responses[i]
            self.responses.append(dict_response)

    def filter_responses(self):
        self.responses = [
            res for res in self.responses if res['diff'].has_differences
        ]

    def clean_response(self, response):
        response['os_response'].sort_instrument_types()
        response['pcs_response'].sort_instrument_types()

    def make_diff(self):
        self.join_responses()
        os_file = './os_response.txt'
        pcs_file = './pcs_response.txt'
        cmd = ["diff", "-u", os_file, pcs_file]

        for response in self.responses:
            self.clean_response(response)
            with open(os_file, 'w') as file_os, open(pcs_file, 'w') as file_pcs:
                file_os.write(response['os_response'].to_json())
                file_pcs.write(response['pcs_response'].to_json())
            diff_string = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)

            poststring = diff_string.stdout.split("\n", 3)[3] if diff_string.stdout else ""
            post = poststring.replace('\n', '<br>').replace("\"", "&#34")
            diff = DiffResponse(post)
            diff.set_has_difference(
                False if not diff_string.stdout else True
            )
            response['diff'] = diff

        self.filter_responses()

    def make_html(self):
        self.html_builder.add_head_tag(
            'link',
            {
                'rel': "stylesheet",
                'href': "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
                "integrity": "sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh",
                "crossorigin": "anonymous",
            }
        )
        self.html_builder.add_head_tag('link', {'rel': "stylesheet", 'href': './index.css'})
        self.html_builder.add_script_tag(src="https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/run_prettify.js")

        rows = []

        for response in self.responses:
            rows.append([
                response['conditions'].get('country'),
                response['conditions'].get('currency'),
                response['conditions'].get('checkout_method'),
                response['os_response'].to_pretty_html_tag(
                    self.html_builder
                ),
                response['pcs_response'].to_pretty_html_tag(
                    self.html_builder
                ),
                response['diff'].to_pretty_html_tag(self.html_builder),
            ])
        self.html_builder.create_table(
            TABLE_HEADERS,
            rows,
            {'class': 'table table-striped table-dark'}
        )
        self.html_builder.create_html_file(
            dest='./payment_options/doc/index.html'
        )


class HtmlBuilder:

    def __init__(self):
        self.head = Html()
        self.head.self_close_tag('meta', attributes=dict(charset='utf-8'))
        self.body = Html()

    def add_head_tag(self, tag_name, attributes=None):
        self.head.self_close_tag(tag_name, attributes=attributes)

    def add_script_tag(self, src):
        self.head.tag_with_content('', name='script', attributes=dict(src=src))

    def get_html_tag(self, tag, content, attributes=None):
        body = Html()
        body.tag_with_content(content, name=tag, attributes=attributes)
        return body.to_raw_html(indent_size=2)

    def create_table(self, headers, rows, attributes=None):

        with self.body.tag('table', attributes=attributes):
            with self.body.tag('thead'):
                for head in headers:
                    self.body.tag_with_content(head, name='th')
            with self.body.tag('tbody'):
                for row in rows:
                    self.create_table_row(row)

    def create_table_row(self, content_list):
        with self.body.tag('tr'):
            for content in content_list:
                self.body.tag_with_content(content, 'td')

    def get_html_built(self):
        return Html.html_template(self.head, self.body).to_raw_html(indent_size=2)

    def create_html_file(self, dest):
        with open(dest, 'w') as file:
            file.write(self.get_html_built())
