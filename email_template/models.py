from django.db import models
from django.utils.translation import ugettext_lazy as _


class EmailTemplate(models.Model):

    NOTIFY_BOARD_NEW_APPLICATION = 1
    NOTIFY_BOARD_VERIFIED_APPLICATION = 2
    NOTIFY_MEMBER_TO_VERIFY_APPLICATION = 3
    NOTIFY_MEMBER_ABOUT_MEMBERSHIP = 4

    TEMPLATE_TYPE_CHOICES = (
        (NOTIFY_BOARD_NEW_APPLICATION, _('Vorstandsbenachrichtigung für neuen Mitgliedsantrag')),
        (NOTIFY_BOARD_VERIFIED_APPLICATION, _('Vorstandsbenachrichtigung für bestätigte bestätigte Email')),
        (NOTIFY_MEMBER_TO_VERIFY_APPLICATION, _('Email mit Bestätigungslink')),
        (NOTIFY_MEMBER_ABOUT_MEMBERSHIP, _('Bestätigung der Mitgliedschaft')),
    )

    template_type = models.CharField(max_length=100,
                                     unique=True,
                                     choices=TEMPLATE_TYPE_CHOICES,
                                     verbose_name=_('Template-Typ'))

    subject = models.CharField(max_length=250, verbose_name=_('Betreff')),
    message = models.TextField(verbose_name=_('Nachricht'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('erstellt am '))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('geändert am'))

    def __str__(self):
        return self.get_template_type_display()

    class Meta:
        verbose_name = _('Email Template')
        verbose_name_plural = _('Email Templates')
