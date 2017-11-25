# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase, client, Client
from django.core.urlresolvers import reverse

# Create your tests here.
from django.utils import timezone

from application.models import MemberApplication
from member.models import Member


class MemberTests(TestCase):
    """
    As a  admin I want to create a Member from a MemberApplicationForm
    """

    def setUp(self):
        self.client = Client()
        my_admin = User.objects.create_superuser('my_admin', 'my_admin@example.org', 'password')
        self.client.login(username=my_admin.username, password='password')

        # Create new Application
        application = MemberApplication()
        application.first_name = 'Florian'
        application.last_name = 'Zyprian'
        application.email = 'florian.zyprian@example.org'
        application.birthday = timezone.now()
        application.phone_number = '0123456789'
        application.street_name = 'A Street'
        application.street_number = '123'
        application.postal_code ='124456'
        application.city = 'A City'
        application.country = 'A Country'
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
                '_selected_action': [unicode(self.application.pk)]}

        response = self.client.post(change_url, data)
        member = Member.objects.get(email='florian.zyprian@example.org')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(member.first_name, 'Florian')
        self.assertEqual(member.last_name, 'Zyprian')
        self.assertEqual(member.email, 'florian.zyprian@example.org')

        application = MemberApplication.objects.get(email='florian.zyprian@example.org')
        self.assertFalse(application.is_new)
        self.assertEqual(application, member.application_form)


