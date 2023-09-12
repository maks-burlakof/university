import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger("email")


def send_email(subject, email_template, to_email, context: dict = None):
    """
        Synchronous script to send one email to address.
    """
    message = render_to_string(email_template, context)
    plain_message = strip_tags(message)
    from_email = settings.EMAIL_HOST_USER
    to_email = [to_email]

    try:
        send_mail(subject, plain_message, from_email, to_email, html_message=message)
    except Exception as err:
        logger.error(f'Error sending email: {err.__class__}: {err}')
        is_success = False
    else:
        logger.info(f'Email sent to {to_email}')
        is_success = True

    return is_success
