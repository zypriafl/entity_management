# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone

from django.contrib import admin
from django.http import JsonResponse, HttpResponse
from django.utils.translation import ugettext_lazy as _

# Register your models here.
from application.models import MemberApplication
from member.models import Member



def accept(modeladmin, request, queryset):
    if len(queryset) > 1:
        status_code = 400
        message =_('Fehler: Mitgliedsanträge müssen einzeln akzeptiert werden.')
        return HttpResponse(message, status=status_code)

    application = queryset[0]
    if not application.is_new:
        status_code = 400
        message = _('Fehler: Mitgliedsantrag wurde bereits bearbeitet.')
        return HttpResponse(message, status=status_code)

    # Create new Member entry
    member = Member()
    member.first_name = application.first_name
    member.last_name = application.last_name
    member.email = application.email
    member.birthday = application.birthday
    member.phone_number = application.phone_number
    member.street_name = application.street_name
    member.street_number = application.street_number
    member.postal_code = application.postal_code
    member.city = application.city
    member.country = application.country
    member.iban = application.iban
    member.bic = application.bic
    member.membership_type = application.membership_type
    member.member_since = timezone.now()

    member.application_form = application
    member.save()

    # Mark as done
    application.is_new = False
    application.save()


def make_done(modeladmin, request, queryset):
    queryset.update(is_new=False)


def make_new(modeladmin, request, queryset):
    queryset.update(is_new=True)


class MemberApplicationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'first_name', 'last_name', 'email', 'membership_type', 'is_new', 'is_verified')
    list_filter = ('is_new',)
    readonly_fields = ('created_at', 'updated_at')
    actions = [make_done, make_new, accept]


admin.site.register(MemberApplication, MemberApplicationAdmin)
accept.short_description = _("Ausgewählter Mitgliedsantrag akzeptieren und neues Mitglied erstellen")
make_done.short_description = _("Ausgewählte Mitgliedsanträge ablehnen")
make_new.short_description = "Ausgewählte Mitgliedsanträge als neu markieren"
