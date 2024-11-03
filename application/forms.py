# -*- coding: utf-8 -*-
from django_recaptcha.fields import ReCaptchaField
from django import forms


class CaptchaLoginForm(forms.Form):
    captcha = ReCaptchaField(label='')
