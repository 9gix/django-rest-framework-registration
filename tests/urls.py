from django.conf.urls import include, url


urlpatterns = [
    url(r'^api-token-auth/', include('rest_framework_registration.urls')),
]
