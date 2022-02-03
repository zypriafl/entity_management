# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext_lazy as _
from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES
from localflavor.generic.models import BICField, IBANField

from application.models import MemberApplication


class Member(models.Model):
    """
    Represents a MemberApplicationForm a potential User can fill out on the web page
    """

    # Options for position types
    BOARD_1 = 'board_1'
    BOARD_2 = 'board_2'
    BOARD_3 = 'board_3'

    POSITION_TYPES = (
        (BOARD_1, _('1. Vorsitzender')),
        (BOARD_2, _('2. Vorsitzender')),
        (BOARD_3, _('Finanzvorstand'))
    )

    # Options for membership types
    ACTIVE = 'active'
    ACTIVE_CHEERLEADING = 'active_cheerleading'
    SUPPORT = 'support'
    INACTIVE = 'inactive'

    MEMBER_TYPES = (
        (ACTIVE, _('Aktiv')),
        (ACTIVE_CHEERLEADING, _('Aktiv - Cheerleading')),
        (SUPPORT, _('Fördermitglied')),
        (INACTIVE, _('Ausgetreten')),
    )

    # Fields that can be populated via the ApplicationForm
    first_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_('Vorname'))
    last_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_('Nachname'))
    gender = models.CharField(max_length=50,
                              null=True,
                              blank=False,
                              choices=MemberApplication.GENDERS,
                              verbose_name='Geschlecht')
    email = models.EmailField(
        null=False,
        blank=False,
        verbose_name=_('E-Mail Adresse'))
    birthday = models.DateField(
        null=False,
        blank=False,
        verbose_name=_('Geburtsdatum'))
    phone_number = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name=_('Telefonnummer'))
    street_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_('Straße'))
    street_number = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        verbose_name=_('Hausnummer'))
    postal_code = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        verbose_name=_('Postleitzahl'))
    city = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_('Stadt'))
    country = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_('Land'))

    iban = IBANField(
        include_countries=IBAN_SEPA_COUNTRIES,
        null=True,
        blank=True,
        verbose_name='IBAN')
    bic = BICField(verbose_name='BIC', null=True, blank=True)

    paid_2018 = models.BooleanField(
        null=True,
        default=False,
        verbose_name='bezahlt 2018?')
    paid_2019 = models.BooleanField(
        null=True,
        default=False,
        verbose_name='bezahlt 2019?')
    paid_2020 = models.BooleanField(
        null=True,
        default=False,
        verbose_name='bezahlt 2020?')
    paid_2021 = models.BooleanField(
        null=True,
        default=False,
        verbose_name='bezahlt 2021?')
    paid_2022 = models.BooleanField(
        null=True,
        default=False,
        verbose_name='bezahlt 2022?')

    membership_type = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        choices=MEMBER_TYPES,
        verbose_name=_('Art der Mitgliedschaft'))

    # Additional Fields for internal management
    position_type = models.CharField(max_length=50,
                                     null=True,
                                     blank=True,
                                     choices=POSITION_TYPES,
                                     verbose_name=_('Position im Vorstand'))
    application_form = models.ForeignKey(MemberApplication,
                                         models.SET_NULL,
                                         null=True,
                                         blank=True,
                                         editable=False,
                                         verbose_name=_('Mitgliedsantrag'))

    member_since = models.DateField(
        null=False,
        blank=False,
        verbose_name=_('Mitlied seit'))

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('erstellt am'))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('geändert am'))

    class Meta:
        verbose_name = _('Mitglied')
        verbose_name_plural = _('Mitglieder')
        ordering = ['-last_name']

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
