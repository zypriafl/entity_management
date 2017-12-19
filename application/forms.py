# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from captcha.fields import ReCaptchaField


class CaptchaLoginForm(forms.Form):
    #secret_answer = forms.CharField(label=_('Login-Frage: Welche universitäre Sportveranstaltung gefällt uns am besten?'))
    captcha = ReCaptchaField(label='')
