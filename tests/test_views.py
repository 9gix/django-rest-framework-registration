from django.test import TestCase
from django.core.urlresolvers import reverse

from django.contrib.auth import get_user_model
from django.core import signing
from django.conf import settings

User = get_user_model()

REGISTRATION_SALT = getattr(settings, 'REGISTRATION_SALT',
                            'rest_framework_registration')

class RegistrationTestCase(TestCase):

    def setUp(self):
        self.registration_data = {
            User.USERNAME_FIELD: 'foo',
            'password': 'bar',
            'email': 'foo@bar.com',
        }

        self.lookup_kwargs = {
            User.USERNAME_FIELD: self.registration_data[User.USERNAME_FIELD]
        }

    def test_registration(self):
        resp = self.client.post(reverse('registration_register'),
                data=self.registration_data)

        new_user = User.objects.get(**self.lookup_kwargs)
        self.assertFalse(new_user.is_active)
        self.assertTrue(
                new_user.check_password(self.registration_data['password']))

        self.assertEqual(new_user.email, self.registration_data['email'])
        self.assertEqual(new_user.username, self.registration_data['username'])

class ActivationWorkflowTestCase(RegistrationTestCase):

    def test_activation(self):
        resp = self.client.post(reverse('registration_register'),
                data=self.registration_data)

        new_user = User.objects.get(**self.lookup_kwargs)
        assert new_user.is_active == False

        activation_key = signing.dumps(
                obj=self.registration_data[User.USERNAME_FIELD],
                salt=REGISTRATION_SALT)

        resp = self.client.get(
            reverse('registration_activate',
                kwargs={'activation_key': activation_key}))

        self.assertRedirects(resp, reverse('registration_activation_complete'))
        self.assertTrue(User.objects.get(**self.lookup_kwargs).is_active)
