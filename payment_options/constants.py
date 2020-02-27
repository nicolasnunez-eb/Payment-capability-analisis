import os


TOKEN = os.environ.get('TOKEN')

COUNTRIES = [
    "AR", "AU", "AT", "BE", "BR", "CA", "CL", "CO",
    "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR",
    "HK", "HU", "IE", "IL", "IT", "JP", "LV", "LT",
    "LU", "MY", "MT", "MX", "NL", "NZ", "NO", "PE", 
    "PH", "PL", "PT", "SG", "SK", "SI", "ES", "SE",
    "CH", "TW", "TH", "GB", "US",
]

CURRENCIES = [
    "ARS", "AUD", "BRL", "CAD", "CHF", "CZK", "DKK", "EUR",
    "GBP", "HKD", "HUF", "ILS", "JPY", "MXN", "MYR", "NOK",
    "NZD", "PHP", "PLN", "SEK", "SGD", "THB", "TWD", "USD",
]

PAYMENT_METHODS = [
    "eventbrite",
    "paypal",
]

ORGANIZATION_ID = 308726941125
EVENT_ID = 62529129309


TABLE_HEADERS = ["Country", "Currency", "Checkout method", "Order service response", "Payment Capability response", "Discrepancy response"]
