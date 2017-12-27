from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.template import Context, Template

from .models import EmailTemplate


def send_template_mail(template_type, recipients, data):
    data["current_domain_url"] = settings.CURRENT_DOMAIN_URL
    template = _get_email_template(template_type)

    for recipient in recipients:
        _send_email(recipient, data, template)


def _get_email_template(template_type):
    try:
        return EmailTemplate.objects.get(template_type=template_type)
    except ObjectDoesNotExist:
        raise ValueError("An email template `{}` does not exist".format(template_type))


def _send_email(recipient, data, template):
    if type(recipient) is User:
        recipient_email = recipient.email
        data["user"] = recipient
    else:
        recipient_email = recipient

    ctx = Context(data)

    return send_mail(_render_email_template(ctx, template.subject),
                     _render_email_template(ctx, template.message),
                     settings.DEFAULT_FROM_EMAIL, [recipient_email])


def _render_email_template(ctx, template_text):
    template = Template(template_text)
    return template.render(ctx)
