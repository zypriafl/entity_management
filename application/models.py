# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


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
    email = models.EmailField(null=False, blank=False, verbose_name='Email Adresse')
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

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('erstellt am'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('geändert am'))

    is_new = models.BooleanField(default=True, editable=False, verbose_name='neu ?')

    # def save(self, *args, **kwargs):
    #     # Forbid editing of Applications
    #     # Todo solf this via permissions
    #     if self.pk:
    #         raise PermissionDenied("Member Application can not be changes")
    #     return super(MemberApplication, self).save(*args, **kwargs)

    def get_model_fields(self):
        return self._meta.fields

    class Meta:
        verbose_name = _('Mitgliedsantrag')
        verbose_name_plural = _('Mitgliedsanträge')
