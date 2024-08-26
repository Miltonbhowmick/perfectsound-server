from decouple import config
from django.core.mail import EmailMultiAlternatives


def send_otp_email(email, otp, reason):

    subject = "OTP for perfectsound."
    from_email = config("PERFECTSOUND_EMAIL_SENDER")
    to_email = email

    text_content = "OTP"

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.send()


def newsletter_email(email, name, description, attachments=None):

    subject = "A Newsletter from you."
    from_email = config("PERFECTSOUND_EMAIL_SENDER")
    to_email = email

    text_content = "Newsletter"

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    if attachments:
        msg.attach_file(attachments.path)
    msg.send()
