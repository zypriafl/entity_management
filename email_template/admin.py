from django.contrib import admin

# Register your models here.
from email_template.models import EmailTemplate

admin.site.register(EmailTemplate)
