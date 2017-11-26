# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Register your models here.
from member.models import Member


class MemberAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'first_name', 'last_name', 'email', 'membership_type', 'position_type')
    readonly_fields = ('application_form', 'created_at', 'updated_at')
    list_filter = ('membership_type',)


admin.site.register(Member, MemberAdmin)
# This is displayed in the top green boy
admin.site.site_header = _('Studylife München e.V.')

# This is shown an the right hand in the tab.
admin.site.site_title = _('Studylife München e.V.')

# This is displayed in the white area between the green header and before the model list begins
# Additional it is show on the left hand in the tab.
admin.site.index_title = _('Verwaltung')
