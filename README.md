# Payment-capability-analisis

## Configure the environment

First create the environment ``` python3 -m venv venv ```

And then install the requirements```pip  install -r requirements.txt```.

After doing this you have to create an environment variable called `token`
that will be the private token generated on eventbrite.com for your user ```export TOKEN="your_token" ```

## Executing the script

First go to constants.py file and replace the `ORGANIZATION_ID` and `EVENT_ID` with yours ids.

To execute the script you have to activate the environment ```source venv/bin/activate```
and then run ```python3 payment_options_script.py```
