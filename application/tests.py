# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase, client, Client
from django.core.urlresolvers import reverse

# Create your tests here.
from django.utils import timezone

from application.models import MemberApplication
from member.models import Member

from application.templatetags.description import TOP_DESCRIPTION, BOTTOM_DESCRIPTION


class MemberTests(TestCase):
    """
    As a  admin I want to create a Member from a MemberApplicationForm
    """

    def setUp(self):
        self.client = Client()
        my_admin = User.objects.create_superuser('my_admin', 'my_admin@example.org', 'password')
        self.client.login(username=my_admin.username, password='password')

        self.example_iban = 'DE 89 37040044 0532013000'.replace(' ', '')
        self.example_bic = '37040044'
        self.gender = MemberApplication.MALE

        # Create new Application
        application = MemberApplication()
        application.first_name = 'Florian'
        application.last_name = 'Zyprian'
        application.gender = self.gender
        application.email = 'florian.zyprian@example.org'
        application.birthday = timezone.now()
        application.phone_number = '0123456789'
        application.street_name = 'A Street'
        application.street_number = '123'
        application.postal_code ='124456'
        application.city = 'A City'
        application.country = 'A Country'
        application.iban = self.example_iban
        application.bic = self.example_bic
        application.membership_type = 'Aktive'
        application.save()

        self.application = application

    def test_application_creation(self):
        self.assertEqual(len(MemberApplication.objects.all()), 1)

    def test_create_member_from_application(self):
        """
        Given a application an admin want to create a Member
        :return:
        """
        self.assertTrue(self.application.is_new)

        change_url = reverse('admin:application_memberapplication_changelist')
        data = {'action': 'accept',
                '_selected_action': [self.application.pk]}

        response = self.client.post(change_url, data)
        member = Member.objects.get(email='florian.zyprian@example.org')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(member.first_name, 'Florian')
        self.assertEqual(member.last_name, 'Zyprian')
        self.assertEqual(member.email, 'florian.zyprian@example.org')
        self.assertEqual(member.gender, self.gender)

        self.assertEqual(member.iban, self.example_iban)
        self.assertEqual(member.bic, self.example_bic)

        application = MemberApplication.objects.get(email='florian.zyprian@example.org')
        self.assertFalse(application.is_new)
        self.assertEqual(application, member.application_form)

    def test_verify_email_accept(self):
        verification_url = reverse('verify', kwargs={'verification_code': self.application.verification_code})
        self.assertFalse(self.application.is_verified)
        response = self.client.get(verification_url)

        self.assertEqual(response.content.decode('utf-8'),
                         ('Dein Mitgliedsantrag wurde bestätigt. '
                          'Wir werden diesen nun prüfen und melden uns bald bei dir.'))

        application = MemberApplication.objects.get(id=self.application.id)
        self.assertTrue(application.is_verified)

    def test_verify_email_accepted_already(self):
        verification_url = reverse('verify', kwargs={'verification_code': self.application.verification_code})
        self.application.is_verified = True
        self.application.save()

        response = self.client.get(verification_url)
        self.assertEqual(response.content.decode('utf-8'), ('Mitgliedsantrag wurde bereits bestätigt.'))

    def test_verify_email_invalid(self):
        invalid_verification_url = reverse('verify', kwargs={'verification_code': 'hsufdkshfkjshkj'})
        response = self.client.get(invalid_verification_url)
        self.assertEqual(response.content.decode('utf-8'), ('Fehler: Üngultiger Code'))

    def test_application_form(self):
        form_url = reverse('admin:application_memberapplication_add')
        response = self.client.get(form_url)
        self.assertContains(response, TOP_DESCRIPTION)
        self.assertContains(response, BOTTOM_DESCRIPTION)




