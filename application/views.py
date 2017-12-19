# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext_lazy as _

# Create your views here.
from django.template.response import TemplateResponse

from application.forms import CaptchaLoginForm
from django.contrib.auth import login

from application.models import MemberApplication


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CaptchaLoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            #secret_answer = form.cleaned_data['secret_answer']

            # Accept Euromasters, Championstrophy, Snowdays and
            # Royalscup independently from spacing and cases
            # if \
            #     ('euro' in secret_answer.lower() and
            #     'master' in secret_answer.lower()) \
            #         or \
            #     ('champions' in secret_answer.lower() and
            #      'trophy' in secret_answer.lower()) \
            #         or \
            #     ('snow' in secret_answer.lower() and
            #      'day' in secret_answer.lower()) \
            #         or \
            #     ('royal' in secret_answer.lower() and
            #      'cup' in secret_answer.lower()):
            if True:
                # login visitor user
                user = User.objects.get(username='visitor')
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return HttpResponseRedirect('/admin/application/memberapplication/add/')

            else:
                # Question not answered correctly.
                return TemplateResponse(request,
                                        "application/index.html",
                                        {'form': form,
                                         'error_message': _('Das ist leider nicht richtig'),
                                         'site_header': _('Studylife München e.V.'),
                                         'site_title': _('Studylife München e.V.'),
                                         'title': _('Verwaltung')})
        else:
            # Captcha not solved.
            return TemplateResponse(request,
                                    "application/index.html",
                                    {'form': form,
                                     'error_message': _('Bitte Captcha eingeben'),
                                     'site_header': _('Studylife München e.V.'),
                                     'site_title': _('Studylife München e.V.'),
                                     'title': _('Verwaltung')})

    # if a GET (or any other method) we'll create a blank form
    form = CaptchaLoginForm()
    return TemplateResponse(request, 
        "application/index.html", 
        {'form': form,
        'site_header': _('Studylife München e.V.'),
        'site_title': _('Studylife München e.V.'),
        'title': _('Verwaltung')})


def impressum(request):
    return TemplateResponse(request, "impressum.html",{})


def verify(request, verification_code):
    # Try to get member application associated to this hash
    try:
        application = MemberApplication.objects.get(verification_code=verification_code)

        if application.is_verified:
            # Return already verified
            message = _('Mitgliedsantrag wurde bereits bestätigt.')
            return HttpResponse(message)

        else :
            # Verifiy application
            application.is_verified = True
            application.save()

            message = _('Dein Mitgliedsantrag wurde bestätigt. Wir werden diesen nun prüfen und melden uns bald bei dir.')
            return HttpResponse(message)

    except ObjectDoesNotExist as e:
        message = _('Fehler: Üngultiger Code')
        return HttpResponse(message, status=400)

    return TemplateResponse(request, "impressum.html", {})



from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/admin/login/?next=/admin/')
