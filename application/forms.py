from django import forms
from captcha.fields import ReCaptchaField


class CaptchaLoginForm(forms.Form):
    secret_answer = forms.CharField(label="What is our favorite university sport event?")
    captcha = ReCaptchaField()
