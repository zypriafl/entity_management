# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from django.test import Client, TestCase
# Create your tests here.
from django.utils import timezone

from application.models import MemberApplication
from application.templatetags.description import (BOTTOM_DESCRIPTION,
                                                  TOP_DESCRIPTION)
from member.models import Member


class MemberTests(TestCase):
    """
    As a  admin I want to create a Member from a MemberApplicationForm
    """
    fixtures = ['fixtures/email_template.json']

    def setUp(self):
        self.client = Client()
        my_admin = User.objects.create_superuser(
            'my_admin', 'my_admin@example.org', 'password')
        self.client.login(username=my_admin.username, password='password')

        # Create Board Member
        Member.objects.create(
            first_name='Max',
            last_name='Mustermann',
            gender=MemberApplication.MALE,
            email='max.mustermann@example.org',
            birthday=timezone.now(),
            member_since=timezone.now(),
            position_type='Vorstand'
        )

        # Create new Application
        self.first_name = 'Florian'
        self.last_name = 'Zyprian'
        self.email = 'florian.zyprian@example.org'
        self.example_iban = 'DE 89 37040044 0532013000'.replace(' ', '')
        self.example_bic = '37040044'
        self.gender = MemberApplication.MALE

        application = MemberApplication()
        application.first_name = self.first_name
        application.last_name = self.last_name
        application.gender = self.gender
        application.email = self.email
        application.birthday = timezone.now()
        application.phone_number = '0123456789'
        application.street_name = 'A Street'
        application.street_number = '123'
        application.postal_code = '124456'
        application.city = 'A City'
        application.country = 'A Country'
        application.iban = self.example_iban
        application.bic = self.example_bic
        application.membership_type = 'Aktive'
        application.save()

        self.application = application

    def test_application_creation(self):
        """
        Test that an application was created and an email was send out
        :return:
        """
        # Test that one message has been sent to the member and one to the
        # board member.
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(
            mail.outbox[0].subject,
            'Bestätige deinen Mitgliedsantrag für Studylife München e.V.')
        self.assertEqual(
            mail.outbox[1].subject,
            'Neuer Mitgliedsantrag für Studylife München e.V.')

        self.assertEqual(len(MemberApplication.objects.all()), 1)

    def test_create_member_from_application(self):
        """
        Given a application an admin want to create a Member
        :return:
        """
        # Empty the test outbox
        mail.outbox = []
        self.assertEqual(len(mail.outbox), 0)
        self.assertTrue(self.application.is_new)

        change_url = reverse('admin:application_memberapplication_changelist')
        data = {'action': 'accept',
                '_selected_action': [self.application.pk]}

        response = self.client.post(change_url, data)
        member = Member.objects.get(email='florian.zyprian@example.org')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(member.first_name, self.first_name)
        self.assertEqual(member.last_name, self.last_name)
        self.assertEqual(member.email, self.email)
        self.assertEqual(member.gender, self.gender)
        self.assertEqual(member.iban, self.example_iban)
        self.assertEqual(member.bic, self.example_bic)

        application = MemberApplication.objects.get(
            email='florian.zyprian@example.org')
        self.assertFalse(application.is_new)
        self.assertEqual(application, member.application_form)

        # Test that one message has been sent to the member.
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            'Deine Mitgliedschaft im Studylife München e.V.')

    def test_verify_email_accept(self):
        # Empty the test outbox
        mail.outbox = []
        verification_url = reverse(
            'verify', kwargs={
                'verification_code': self.application.verification_code})
        self.assertFalse(self.application.is_verified)
        response = self.client.get(verification_url)

        self.assertEqual(
            response.content.decode('utf-8'),
            ('Dein Mitgliedsantrag wurde bestätigt. '
             'Wir werden diesen nun prüfen und melden uns bald bei dir.'))

        application = MemberApplication.objects.get(id=self.application.id)
        self.assertTrue(application.is_verified)

        # Test that one message has been sent to the member and one to the
        # board member.
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            'Bestätigung eines Mitgliedsantrag für Studylife München e.V.')

    def test_verify_email_accepted_already(self):
        verification_url = reverse(
            'verify', kwargs={
                'verification_code': self.application.verification_code})
        self.application.is_verified = True
        self.application.save()

        # Empty the test outbox
        mail.outbox = []

        response = self.client.get(verification_url)
        self.assertEqual(
            response.content.decode('utf-8'),
            ('Mitgliedsantrag wurde bereits bestätigt.'))

        # Test that no message has been sent.
        self.assertEqual(len(mail.outbox), 0)

    def test_verify_email_invalid(self):
        invalid_verification_url = reverse(
            'verify', kwargs={
                'verification_code': 'hsufdkshfkjshkj'})
        response = self.client.get(invalid_verification_url)
        self.assertEqual(
            response.content.decode('utf-8'),
            ('Fehler: Üngultiger Code'))

    def test_application_form(self):
        form_url = reverse('admin:application_memberapplication_add')
        response = self.client.get(form_url)
        self.assertContains(response, TOP_DESCRIPTION)
        self.assertContains(response, BOTTOM_DESCRIPTION)
