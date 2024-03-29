"""entity_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import re_path
from django.contrib import admin
from django.views.generic import TemplateView

from application import views

urlpatterns = [
    re_path(r'^logout/$', views.logout_view),

    re_path(r'^admin/', admin.site.urls),
    re_path(r'^impressum/', views.impressum),
    re_path(r'^reimbursement/', TemplateView.as_view(template_name='accounting/reimbursement.html')),
    re_path(r'^verify/(?P<verification_code>[-\w]+)/$', views.verify, name='verify'),
    re_path(r'^', views.index),


]
