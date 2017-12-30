# -*- coding: utf-8 -*-


from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES
from localflavor.generic.models import BICField, IBANField

from email_template.helpers import send_template_mail
from email_template.models import EmailTemplate


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

    first_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Vorname')
    last_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Nachname')
    gender = models.CharField(
        max_length=50,
        null=True,
        blank=False,
        choices=GENDERS,
        verbose_name='Geschlecht')
    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
        verbose_name='E-Mail Adresse')
    verification_code = models.CharField(
        max_length=64, null=False, unique=True, editable=False)

    birthday = models.DateField(
        null=False,
        blank=False,
        verbose_name='Geburtsdatum')
    phone_number = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Telefonnummer')
    street_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Straße',
        help_text='Bitte die Münchner Adresse angeben (falls vorhanden).')
    street_number = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        verbose_name='Hausnummer',
        help_text='Bitte die Münchner Adresse angeben (falls vorhanden).')
    postal_code = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        verbose_name='Postleitzahl',
        help_text='Bitte die Münchner Adresse angeben (falls vorhanden).')
    city = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Stadt',
        help_text='Bitte die Münchner Adresse angeben (falls vorhanden).')
    country = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        default='Deutschland',
        verbose_name='Land')

    iban = IBANField(include_countries=IBAN_SEPA_COUNTRIES,
                     null=True, verbose_name='Deine IBAN')
    bic = BICField(null=True, verbose_name='Deine BIC')

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

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('erstellt am'))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('geändert am'))

    is_new = models.BooleanField(
        default=True,
        editable=False,
        verbose_name='neu ?')
    is_verified = models.BooleanField(
        default=False,
        editable=False,
        verbose_name='Bestätigt via Email ?')

    def save(self, *args, **kwargs):
        # Generate verify code if not exist yet
        if not self.verification_code:
            self.verification_code = get_random_string(64)

        # Load board members that needs to notified
        Member = apps.get_model('member', 'Member')
        board_members = list(
            Member.objects.filter(
                position_type__isnull=False).values_list(
                'email', flat=True))

        if not self.pk:
            # Send Email to new Member
            verify_path = reverse(
                'verify', kwargs={
                    'verification_code': self.verification_code})
            verify_url = '{}{}'.format(
                settings.CURRENT_DOMAIN_URL, verify_path)
            send_template_mail(EmailTemplate.NOTIFY_MEMBER_TO_VERIFY_APPLICATION,
                               [self.email],
                               {'member_application': self,
                                'verify_url': verify_url})

            # Notify board members about new applications
            Member = apps.get_model('member', 'Member')

            send_template_mail(EmailTemplate.NOTIFY_BOARD_NEW_APPLICATION,
                               board_members,
                               {"member_application": self})

        # Notify board members about verified applications
        if self.pk:
            old_self = MemberApplication.objects.get(email=self.email)
            if not old_self.is_verified and self.is_verified:
                send_template_mail(
                    EmailTemplate.NOTIFY_BOARD_VERIFIED_APPLICATION, board_members, {
                        "member_application": self})

        return super(MemberApplication, self).save(*args, **kwargs)

    def __str__(self):
        return 'Mitgliedsantrag vom {:%d.%m.%Y}'.format(self.created_at)

    class Meta:
        verbose_name = _('Mitgliedsantrag')
        verbose_name_plural = _('Mitgliedsanträge')
