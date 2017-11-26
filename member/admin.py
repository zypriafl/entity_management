# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

# Register your models here.
from member.models import Member


def csv_export(modeladmin, request, queryset):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mitglieder.csv"'
    writer = csv.writer(response)
    writer.writerow(['Vorname',
                     'Nachname',
                     'Email',
                     'Geburtsdatum',
                     'Telefonnummer',
                     'Straße',
                     'Hausnummer',
                     'Postleitzahl',
                     'Stadt',
                     'Land',
                     'Art der Mitgliedschaft',
                     'Mitglied seit',
                     ])

    for member in queryset:
        writer.writerow([member.first_name,
                        member.last_name,
                        member.email,
                        member.birthday,
                        member.phone_number,
                        member.street_name,
                        member.street_number,
                        member.postal_code,
                        member.city,
                        member.country,
                        member.membership_type,
                        member.member_since])

    return response


class MemberAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'first_name', 'last_name', 'email', 'membership_type', 'position_type')
    readonly_fields = ('application_form', 'created_at', 'updated_at')
    list_filter = ('membership_type',)
    actions = [csv_export]


admin.site.register(Member, MemberAdmin)
# This is displayed in the top green boy
admin.site.site_header = _('Studylife München e.V.')

# This is shown an the right hand in the tab.
admin.site.site_title = _('Studylife München e.V.')

# This is displayed in the white area between the green header and before the model list begins
# Additional it is show on the left hand in the tab.
admin.site.index_title = _('Verwaltung')


csv.short_description = "Ausgewählte Mitglieder als csv exportieren"