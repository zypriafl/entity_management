# -*- coding: utf-8 -*-
from captcha.fields import ReCaptchaField
from django import forms


class CaptchaLoginForm(forms.Form):
    captcha = ReCaptchaField(label='')
