import requests

from django.conf import settings


KHALTI_INITIATE_URL = "https://dev.khalti.com/api/v2/epayment/initiate/"


def initiate_khalti_payment(payload):

    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        KHALTI_INITIATE_URL,
        json=payload,
        headers=headers,
        timeout=30,
    )

    return response