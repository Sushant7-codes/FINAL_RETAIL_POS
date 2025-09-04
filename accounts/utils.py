#import send_mail
from django.conf import settings
from django.core.mail import send_mail


def is_email_valid(email):
    from django.core.validators import validate_email

    try:
        validate_email(email)
        return True
    except Exception :
        return False
    

def forgot_password_email(email):
    from .models import OTP
    
    try:
        new_otp = OTP.generate_otp(email)
    except Exception as e:
        raise Exception(str(e))
    
    subject = "Password Reset"
    message=f"""
    Use the OTP {new_otp} to reset your password
    OR
    Follow the link to goto otp confirmation page: http://127.0.0.1:8000/accounts/otp-confirmation/
    """
    send_mail(subject, message, settings.EMAIL_HOST_USER ,[email])