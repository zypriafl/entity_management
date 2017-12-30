# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EmailTemplateConfig(AppConfig):
    name = 'email_template'
    verbose_name = _('Email Templates')
