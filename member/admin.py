# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Register your models here.
from member.models import Member

class MemberAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'first_name', 'last_name', 'email', 'membership_type')
    readonly_fields = ('application_form', 'created_at', 'updated_at')


admin.site.register(Member, MemberAdmin)
admin.site.site_header = _('Studylife München e.V.')
admin.site.site_title = _('Verwaltung')
admin.site.index_title = _('Studylife München e.V.')
