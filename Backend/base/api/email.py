from datetime import date, timedelta, timezone
from django.core.mail import send_mail
import random
import string
from .models import *
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.hashers import make_password;
from django.utils import timezone
from rest_framework.response import Response

def generate_otp(length=6):
    try:
        characters = string.digits
        otp = ''.join(random.choice(characters) for _ in range(length))
        return otp
    except Exception as e :
        return e

def send_otp(email):
    try: 
        otp = generate_otp()
        print(otp)
        hashed_otp = make_password(otp)
        exp_time = timezone.now() + timedelta(minutes=3)
        User.objects.filter(email = email).update(otp=hashed_otp, otp_expiry_time = exp_time)
        subject = "REBOOT ROBOTICS ACADEMY - Reset Password"
        message = f'Your OTP is: {otp} OTP will Expire after 3 minutes'
        from_email = getattr(settings, 'EMAIL_HOST_USER', None)
        print(from_email)
        recipient_list = [email]
        return send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
    except Exception as e:
        return Response({
                'status': 500,
                'error' : str(e)
            })
