# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.core.mail import mail_managers, mail_admins, send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_true(value):
    if not value:
        raise ValidationError(
            _('Dieses Feld muss ausgewählt sein'),
        )


class MemberApplication(models.Model):
    """
    Represents a MemberApplicationForm a potential User can fill out on the web page
    """

    # Options for membership types
    ACTIVE = 'active'
    ACTIVE_CHEERLEADING = 'active_cheerleading'
    SUPPORT = 'support'

    MEMBER_TYPES = (
        (ACTIVE, _('Aktiv')),
        (ACTIVE_CHEERLEADING, _('Aktiv - Cheerleading')),
        (SUPPORT, _('Fördermitglied'))
    )

    first_name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Vorname')
    last_name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Nachname')
    email = models.EmailField(null=False, blank=False, unique=True, verbose_name='Email Adresse')
    birthday = models.DateField(null=False, blank=False, verbose_name='Geburtsdatum')
    phone_number = models.CharField(max_length=50, null=False, blank=False, verbose_name='Telefonnummer')
    street_name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Straße')
    street_number = models.CharField(max_length=25, null=False, blank=False, verbose_name='Hausnummer')
    postal_code = models.CharField(max_length=25, null=False, blank=False, verbose_name='Postleitzahl')
    city = models.CharField(max_length=100, null=False, blank=False, verbose_name='Stadt')
    country = models.CharField(max_length=100, null=False, blank=False, verbose_name='Land')
    membership_type = models.CharField(max_length=50,
                                       null=False,
                                       blank=False,
                                       choices=MEMBER_TYPES,
                                       verbose_name='Art der Mitgliedschaft')
    wants_to_be_member = models.BooleanField(default=False,
                                             blank=False,
                                             validators=[validate_true],
                                             verbose_name=_('Ich möchte zum nächstmöglichen Zeitpunkt Mitglied '
                                                            'im Studylife München e.V werden. Um den Mitgliedsantrag '
                                                            'abzuschicken klicke auf "Sichern".'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('erstellt am'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('geändert am'))

    is_new = models.BooleanField(default=True, editable=False, verbose_name='neu ?')

    def save(self, *args, **kwargs):
        # Notfify baord members about new applications
        if not self.pk:
            Member = apps.get_model('member', 'Member')
            board_member = (Member.objects.filter(position_type__isnull=False))

            for member in board_member:
                send_mail(_('Neuer Mitgliedsantrag für Studylife München e.V. '),
                          _('Neuer Mitgliedsantrag von {} {} eingegangen. '
                            'Um den Antrag zu sehen gehe auf: https://studylife-muenchen.de'.format(self.first_name, self.last_name)),
                          'noreply@studylife-muenchen.de',
                          [member.email])
        return super(MemberApplication, self).save(*args, **kwargs)

    def __str__(self):
        return 'Mitgliedsantrag vom {:%d.%m.%Y}'.format(self.created_at)


    class Meta:
        verbose_name = _('Mitgliedsantrag')
        verbose_name_plural = _('Mitgliedsanträge')
