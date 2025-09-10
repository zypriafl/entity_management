# -*- coding: utf-8 -*-
import csv

from django.contrib import admin
from django.contrib.admin.models import DELETION, LogEntry
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _

# Register your models here.
from member.models import Member


class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    # readonly_fields = LogEntry._meta.get_all_field_names()

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (reverse('admin:%s_%s_change' % (
                ct.app_label, ct.model), args=[obj.object_id]), escape(obj.object_repr), )
        return link

    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')


admin.site.register(LogEntry, LogEntryAdmin)


def csv_export(modeladmin, request, queryset):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mitglieder.csv"'
    writer = csv.writer(response)
    writer.writerow(['Geschlecht',
                     'Vorname',
                     'Nachname',
                     'Email',
                     'Geburtsdatum',
                     'Telefonnummer',
                     'Straße',
                     'Hausnummer',
                     'Postleitzahl',
                     'Stadt',
                     'Land',
                     'IBAN',
                     'BIC',
                     'Art der Mitgliedschaft',
                     'Mitglied seit',
                     ])

    for member in queryset:
        writer.writerow([
                        member.gender,
                        member.first_name,
                        member.last_name,
                        member.email,
                        member.birthday,
                        member.phone_number,
                        member.street_name,
                        member.street_number,
                        member.postal_code,
                        member.city,
                        member.country,
                        member.iban,
                        member.bic,
                        member.membership_type,
                        member.member_since])

    return response


class MemberAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'gender',
        'first_name',
        'last_name',
        'email',
        # 'paid_2021',
        # 'paid_2022',
        # 'paid_2023',
        'paid_2024',
        'paid_2025',
        'paid_2026',
        'member_since',
        'member_exited',
        'membership_type',
        'position_type')
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
