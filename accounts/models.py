from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics", null=True, blank=True)

    def __str__(self):
        return self.username
    

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp=models.CharField(max_length=10, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    @staticmethod
    def generate_otp(email):
        import random
        
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            raise Exception("User does not exist")
        
        new_otp = OTP.objects.create(
            user=user,otp=random.randint(100000,999999)
            )
        new_otp.save()
        return new_otp.otp

    def is_expired(self):
        from django.utils import timezone
        import datetime
        
        now = timezone.now()
        return now - self.created_at > datetime.timedelta(
            minutes=5
        )
        
    @staticmethod
    def check_otp(otp_value):
        otp_record = OTP.objects.filter(otp=otp_value).first()
        if otp_record and not otp_record.is_expired():
            user_id = otp_record.user.id
            otp_record.delete()
            return user_id
        return None        
        
    def __str__(self):
        return self.otp