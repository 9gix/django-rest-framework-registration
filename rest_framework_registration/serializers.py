from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email',)

    def create(self, validated_data):
        is_active = validated_data.pop('is_active')
        user = User.objects.create_user(**validated_data)
        user.is_active = is_active
        user.save()
        return user
