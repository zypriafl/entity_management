# -*- coding: utf-8 -*-
from captcha.fields import ReCaptchaField
from django import forms
from django.utils.translation import ugettext_lazy as _


class CaptchaLoginForm(forms.Form):
    #secret_answer = forms.CharField(label=_('Login-Frage: Welche universitäre Sportveranstaltung gefällt uns am besten?'))
    captcha = ReCaptchaField(label='')
