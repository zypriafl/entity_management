# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.core.mail import mail_managers, mail_admins, send_mail
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from localflavor.generic.models import IBANField, BICField
from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES

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

    # Options for gender
    FEMALE = 'female'
    MALE = 'male'

    MEMBER_TYPES = (
        (ACTIVE, _('Aktiv')),
        (ACTIVE_CHEERLEADING, _('Aktiv - Cheerleading')),
        (SUPPORT, _('Fördermitglied'))
    )

    GENDERS = (
        (FEMALE, _('Frau')),
        (MALE, _('Mann')),
    )

    gender = models.CharField(max_length=50, null=True, blank=False, choices=GENDERS, verbose_name='Geschlecht')
    first_name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Vorname')
    last_name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Nachname')
    email = models.EmailField(null=False, blank=False, unique=True, verbose_name='Email Adresse', help_text='Bitte deine TUM Adresse angeben (falls vorhanden)')
    verification_code = models.CharField(max_length=64, null=False, unique=True, editable=False)

    birthday = models.DateField(null=False, blank=False, verbose_name='Geburtsdatum')
    phone_number = models.CharField(max_length=50, null=False, blank=False, verbose_name='Telefonnummer')
    street_name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Straße', help_text='Bitte deine München Addresse angeben (falls vorhanden).')
    street_number = models.CharField(max_length=25, null=False, blank=False, verbose_name='Hausnummer', help_text='Bitte deine München Addresse angeben (falls vorhanden).')
    postal_code = models.CharField(max_length=25, null=False, blank=False, verbose_name='Postleitzahl', help_text='Bitte deine München Addresse angeben (falls vorhanden).')
    city = models.CharField(max_length=100, null=False, blank=False, verbose_name='Stadt', help_text='Bitte deine München Addresse angeben (falls vorhanden).')
    country = models.CharField(max_length=100, null=False, blank=False, default='Deutschland', verbose_name='Land')

    iban = IBANField(include_countries=IBAN_SEPA_COUNTRIES, null=True, blank=True, verbose_name='Deine IBAN')
    bic = BICField( null=True, blank=True, verbose_name='Deine BIC')

    membership_type = models.CharField(max_length=50,
                                       null=False,
                                       blank=False,
                                       choices=MEMBER_TYPES,
                                       verbose_name='Art der Mitgliedschaft')
    wants_to_be_member = models.BooleanField(default=False,
                                             null=False,
                                             blank=False,
                                             validators=[validate_true],
                                             )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('erstellt am'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('geändert am'))

    is_new = models.BooleanField(default=True, editable=False, verbose_name='neu ?')
    is_verified = models.BooleanField(default=False, editable=False, verbose_name='Bestätigt via Email ?')

    def save(self, *args, **kwargs):
        # Generate verify code if not exist yet
        if not self.verification_code:
            self.verification_code = get_random_string(64)

        # Load board members that needs to notified
        Member = apps.get_model('member', 'Member')
        board_member = (Member.objects.filter(position_type__isnull=False))

        # Send Email to new Member
        if not self.pk:
            send_mail(_('Bestätige deinen Mitgliedsantrag für Studylife München e.V. '),
                      _('Dein Mitgliedsantrag ist eingegangen. '
                        'Bitte bestätige deinen Mitgliedsantrag mit '
                        'einem Klick auf folgenden Link https://studylife-muenchen.de/verify/{}/'.format(self.verification_code)),
                      'noreply@studylife-muenchen.de',
                      [self.email])
        #print('https://studylife-muenchen.de/verify/{}/'.format(self.verification_code))

        # Notfify board members about verified applications
        if self.pk:
            old_self = MemberApplication.objects.get(email=self.email)
            if not old_self.is_verified and self.is_verified:
                for member in board_member:
                    send_mail(_('Bestätigung eines Mitgliedsantrag für Studylife München e.V. '),
                              _('Der Mitgliedsantrag von {} {} würde bestätigt. '
                                'Um den Antrag zu bearbeiten gehe auf: https://studylife-muenchen.de'.format(self.first_name,
                                                                                                        self.last_name)),
                              'noreply@studylife-muenchen.de',
                              [member.email])

        # Notfify board members about new applications
        if not self.pk:
            Member = apps.get_model('member', 'Member')
            board_member = (Member.objects.filter(position_type__isnull=False))

            for member in board_member:
                send_mail(_('Neuer Mitgliedsantrag für Studylife München e.V. '),
                          _('Neuer Mitgliedsantrag von {} {} eingegangen. '
                            'Um den Antrag zu bearbeiten gehe auf: https://studylife-muenchen.de'.format(self.first_name, self.last_name)),
                          'noreply@studylife-muenchen.de',
                          [member.email])

        # Ensure group name is not longer than 80 characters
        return super(MemberApplication, self).save(*args, **kwargs)

    def __str__(self):
        return 'Mitgliedsantrag vom {:%d.%m.%Y}'.format(self.created_at)


    class Meta:
        verbose_name = _('Mitgliedsantrag')
        verbose_name_plural = _('Mitgliedsanträge')
