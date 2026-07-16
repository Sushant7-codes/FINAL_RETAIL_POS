from django.conf import settings
from django.core.mail import EmailMessage

# from django.core.mail import send_mail

# def send_otp(email, new_otp, purpose="forgot"):
#     if purpose == "register":
#         subject = "Verify Your Email - Registration"
#         message = f"""
#         Welcome! 🎉
        
#         Use the OTP {new_otp} to verify your email and complete registration.
        
#         This OTP will expire in 5 minutes.
#         """
#     else:  # default → forgot password
#         subject = "Password Reset OTP"
#         message = f"""
#         You requested to reset your password.
        
#         Use the OTP {new_otp} to reset your password
#         OR
#         Go to the OTP confirmation page: http://127.0.0.1:8000/accounts/otp-confirmation/
        
#         This OTP will expire in 5 minutes.
#         """

#     print("EMAIL_HOST_USER:", settings.EMAIL_HOST_USER)
#     print("EMAIL_HOST_PASSWORD exists:", bool(settings.EMAIL_HOST_PASSWORD))

#     send_mail(subject, message, settings.EMAIL_HOST_USER, [email])


def send_otp(email, new_otp, purpose="forgot"):

    if purpose == "register":
        subject = "Verify Your Email"
        message = f"Your OTP is {new_otp}"
    else:
        subject = "Password Reset OTP"
        message = f"Your OTP is {new_otp}"

    print("EMAIL:", settings.EMAIL_HOST_USER)

    try:
        mail = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
        )

        mail.send(fail_silently=False)

        print("EMAIL SENT SUCCESSFULLY")

    except Exception as e:
        print("EMAIL ERROR:")
        print(type(e))
        print(e)
        raise