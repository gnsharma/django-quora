import logging
import sys

from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def send_feedback_email(email, message):
    # with mail.get_connection() as connection:
    c = {'email': email, 'message': message}

    email_subject = render_to_string('quora/feedback/email/feedback_email_subject.txt', c).replace('\n', '')
    email_body = render_to_string('quora/feedback/email/feedback_email_body.txt', c)

    # email_final = EmailMessage(email_subject, email_body, settings.EMAIL_HOST_USER, [email], connection, headers={'Reply-To': email})
    # return email_final.send(fail_silently=False)

    logging.info("email ready, calling Send")

    mail.send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
