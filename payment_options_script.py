import urllib3
import asyncio

from async_context_manager import AsyncContextManager

from payment_options.api_executor import OrderServiceCommand

from payment_options.logger import ResponseManager

from payment_options.utils import (
    get_combinations,
    split_list,
)


with AsyncContextManager() as loop:
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    combinations = get_combinations()
    order_service_command = OrderServiceCommand()
    response_manager = ResponseManager()
    checkout_settings = []

    #### Creating checkout settings for the ORGANIZATION ID

    tasks = [
        order_service_command.get_checkout_setting_id(country, currency, checkout_method)
        for country, currency, checkout_method in combinations
    ]
    # tasks = [
    #     order_service_command.get_checkout_setting_id("US", "USD", "eventbrite"),
    #     order_service_command.get_checkout_setting_id("AR", "ARS", "eventbrite")
    # ]
    task_splitted = split_list(tasks, 108)


    for tasks in list(task_splitted):
        responses = loop.run_until_complete(asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED))
        checkout_settings.extend([
                response.result() for response in responses[0]
            ])

    #####


    checkout_settings = [
        checkout_setting
        for checkout_setting in checkout_settings
        if checkout_setting.get('checkout_setting_id')
    ]

    for checkout_setting in checkout_settings:
        response_manager.add_conditions(checkout_setting)


    #### Once the checkout settings were created we configure the event with every checkout setting
    #### and then retreive the payment options, first from order_service


    order_service_command.change_checkout_setting_from_event(
        checkout_settings,
        response_manager.add_order_service_response,
    )

    yes = ['yes','y', 'ye', '']
    while True:
        print("Please turn on the USE_PCS_TO_GET_PAYMENT_CAPABILITIES FF")
        key = input("Continue? [Y]: ").lower()
        if key in yes:
            break

    #### And when we activate the FF we retreive the same data but from Payment capability service


    order_service_command.change_checkout_setting_from_event(
        checkout_settings,
        response_manager.add_pcs_response,
    )

    #### Here we create an html file that only shows the responses that has a discrepancy between OS and PCS
    response_manager.make_diff()
    response_manager.make_html()
