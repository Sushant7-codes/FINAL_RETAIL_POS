from background_task import background
from django.conf import settings
from django.core.mail import send_mail


@background(schedule=3)
def send_otp(email,new_otp):
        subject = "Password Reset"
        message=f"""
        Use the OTP {new_otp} to reset your password
        OR
        Follow the link to goto otp confirmation page: http://127.0.0.1:8000/accounts/otp-confirmation/
        """
        
        send_mail(subject, message, settings.EMAIL_HOST_USER ,[email])
        
        