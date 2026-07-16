import requests
from django.conf import settings


def send_otp(email, new_otp, purpose="forgot"):

    if purpose == "register":
        subject = "Verify Your Email - Registration"

        message = f"""
Welcome!

Use the OTP below to verify your account.

OTP: {new_otp}

This OTP expires in 5 minutes.
"""

    else:
        subject = "Password Reset OTP"

        message = f"""
You requested to reset your password.

OTP: {new_otp}

This OTP expires in 5 minutes.
"""

    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": "onboarding@resend.dev",
            "to": [email],
            "subject": subject,
            "text": message,
        },
        timeout=15,
    )

    print(response.status_code)
    print(response.text)

    response.raise_for_status()