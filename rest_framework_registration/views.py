from django.conf import settings
from django.core import signing
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.views import generic as dj_generic
from django.shortcuts import redirect

from rest_framework import generics as drf_generics

from . import serializers
from . import signals


ACCOUNT_ACTIVATION_DAYS = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 7)
REGISTRATION_SALT = getattr(settings, 'REGISTRATION_SALT',
                            'rest_framework_registration')

User = get_user_model()


class RegistrationView(drf_generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    email_body_template = 'registration/activation_email_body.txt'
    email_subject_template = 'registration/activation_email_subject.txt'

    def get_activation_key(self, user):
        return signing.dumps(getattr(user, User.USERNAME_FIELD),
                             salt=REGISTRATION_SALT)

    def send_activation_email(self, user):
        ctx = {
            'activation_key': self.get_activation_key(user),
            'expiration_days': ACCOUNT_ACTIVATION_DAYS,
            'site': get_current_site(self.request),
            'user': user,
        }
        subject = render_to_string(self.email_subject_template)
        subject = ' '.join(subject.splitlines())
        message = render_to_string(self.email_body_template, ctx)

        user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def create_inactive_user(self, serializer):
        user = serializer.save(is_active=False)
        self.send_activation_email(user)
        return user

    def perform_create(self, serializer):
        user = self.create_inactive_user(serializer)
        signals.user_registered.send(sender=self.__class__, user=user,
                                     request=self.request)


class ActivationView(dj_generic.TemplateView):
    template_name = 'registration/activate.html'

    def get(self, request, *args, **kwargs):
        activated_user = self.activate(request, *args, **kwargs)
        if activated_user:
            signals.user_activated.send(
                sender=self.__class__,
                user=activated_user,
                request=self.request)
            success_url = self.get_success_url(activated_user)
            try:
                to, args, kwargs = success_url
                return redirect(to, *args, **kwargs)
            except ValueError:
                return redirect(success_url)
        return super().get(request, *args, **kwargs)

    def get_success_url(self, user):
        return ('registration_activation_complete', (), {})

    def activate(self, request, *args, **kwargs):
        username = self.validate_key(kwargs.get('activation_key'))

        if username is None:
            return False

        try:
            user = User.objects.get(**{
                User.USERNAME_FIELD: username,
                'is_active': False,
            })
        except User.DoesNotExist:
            return False

        user.is_active = True
        user.save()
        return user

    def validate_key(self, activation_key):
        try:
            username = signing.loads(
                activation_key,
                salt=REGISTRATION_SALT,
                max_age=ACCOUNT_ACTIVATION_DAYS * 86400)
        except signing.BadSignature:
            username = None

        return username

    def get_user(self, username):
        try:
            user = User.objects.get(**{
                User.USERNAME_FIELD: username,
                'is_active': False,
            })
        except User.DoesNotExist:
            user = None
        return user
