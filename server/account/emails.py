from decouple import config
from django.core.mail import EmailMultiAlternatives


def send_otp_email(email, otp, reason):

    subject = "OTP for perfectsound."
    from_email = config("PERFECTSOUND_EMAIL_SENDER")
    to_email = email

    text_content = "OTP"

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.send()
