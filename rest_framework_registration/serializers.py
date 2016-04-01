from django.contrib.auth import get_user_model
from rest_framework import serializers

from registration.models import RegistrationProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ('username', 'password', 'email',)
