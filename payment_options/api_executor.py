import aiohttp
import json
import requests

from payment_options.constants import (
    EVENT_ID,
    ORGANIZATION_ID,
    TOKEN,
)


class ApiExecutor():

    URL_BASE = "https://www.evbqaapi.com/v3"
    HEADERS = {'Content-Type': 'application/json'}

    def request_post(self, url, body):
        return requests.post(
            url,
            params={
                'token': TOKEN,
            },
            data=json.dumps(body),
            headers=self.HEADERS,
            verify=False,
        )

    async def async_request_post(self, url, body):
        async with aiohttp.ClientSession() as session:
            return await session.post(
                url="{url}/?token={token}".format(url=url, token=TOKEN),
                data=json.dumps(body),
                headers=self.HEADERS,
                ssl=False,
            )


class OrderServiceApiExecutor(ApiExecutor):

    async def create_checkout_setting_for_organization(
        self, body, organization_id
    ):
        return await self.async_request_post(
            url=self._get_create_checkout_setting_url(organization_id),
            body=body,
        )

    def update_checkout_setting_for_event(self, body, event_id):
        return self.request_post(
            url=self._get_update_event_checkout_setting_url(event_id),
            body=body
        )

    def get_payment_options_from_order_service(self, body, event_id):
        return requests.get(
            self._get_obtain_payment_options_url(event_id),
            params={
                'token': TOKEN,
            },
            data=json.dumps(body),
            headers=self.HEADERS,
            verify=False,
        )

    def _get_create_checkout_setting_url(self, organization_id):
        url = "{base}/organizations/{organization_id}/checkout_settings/"
        return url.format(
                base=self.URL_BASE, organization_id=organization_id
            )

    def _get_update_event_checkout_setting_url(self, event_id):
        url = "{base}/events/{event_id}/checkout_settings/"
        return url.format(
                base=self.URL_BASE, event_id=event_id
            )

    def _get_obtain_payment_options_url(self, event_id):
        url = "{base}/events/{event_id}/payment_options/"
        return url.format(
                base=self.URL_BASE, event_id=event_id
            )


class OrderServiceCommand:

    def __init__(self):
        self.api_executor = OrderServiceApiExecutor()

    async def _create_checkout_method(self, country, currency, checkout_method):
        body = {
            'checkout_settings': {
                'checkout_method': checkout_method,
                'country_code': country,
                'currency_code': currency,
            }
        }

        if checkout_method == 'paypal':
            body.update({"paypal_email": "federico-personal@evbqa.com"})

        return await self.api_executor.create_checkout_setting_for_organization(
            body=body,
            organization_id=ORGANIZATION_ID
        )

    async def get_checkout_setting_id(self, country, currency, checkout_method):
        create_checkout_setting_response = await self._create_checkout_method(
                    country, currency, checkout_method
                )
        response_json = await create_checkout_setting_response.text()

        result = {
                    "country": country,
                    "currency": currency,
                    "checkout_method": checkout_method
                }

        if create_checkout_setting_response.status == 200:
            result.update(
                {
                    "checkout_setting_id": json.loads(response_json).get('id')
                }
            )
        elif json.loads(response_json).get('error') == 'DUPLICATE':
            result.update(
                {
                    "checkout_setting_id": json.loads(response_json).get('error_description').split(' ')[-1][:-1]
                }
            )

        return result

    def _get_payment_options_from_checkout_setting_id(
        self, checkout_setting_id
    ):

        self.api_executor.update_checkout_setting_for_event(
            body={
                "checkout_settings_ids": [checkout_setting_id]
            },
            event_id=EVENT_ID
        )

        while True:
            response = \
                self.api_executor.get_payment_options_from_order_service(
                    body={},
                    event_id=EVENT_ID
                )
            if response.status_code == 200:
                return response

    def change_checkout_setting_from_event(self, checkout_settings, function):
        for checkout_setting in checkout_settings:
            if checkout_setting.get('checkout_setting_id'):
                response = self._get_payment_options_from_checkout_setting_id(
                    checkout_setting.get('checkout_setting_id')
                )
                function(response.json())
