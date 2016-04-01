from django.conf.urls import url
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    url(r'^registrations/$',
        views.RegistrationView.as_view(), name='registration_register'),
    url(r'^activations/(?P<activation_key>[-:\w]+)/$',
        views.ActivationView.as_view(), name='registration_activate'),
    url(r'^activation-complete/$',
        TemplateView.as_view(
            template_name='registration/activation_complete.html'
        ),
        name='registration_activation_complete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
