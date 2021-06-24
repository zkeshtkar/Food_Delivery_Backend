from rest_framework import serializers, exceptions

from .models import User
from .validators import EmailValidator, PhoneValidator

PASSWORD_LENGTH = 8


class RegisterWithEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50, min_length=5, validators=[EmailValidator])
    password = serializers.CharField(min_length=8, max_length=30)

    def validate_password(self, password):
        if not any(ch.isdigit() for ch in password):
            raise exceptions.ValidationError(detail='Password must contain digit.')
        if not any(ch.isalpha() for ch in password):
            raise exceptions.ValidationError(detail='Password must contain alpha.')
        if len(password) < PASSWORD_LENGTH:
            raise exceptions.ValidationError(detail='Password must be more than 8 character.')

    class Meta:
        model = User
        fields = (
            'password', 'email',)


class RegisterWithPhoneSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=11, validators=[PhoneValidator])
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'password', 'phone',)

    def validate_password(self, password):
        if not any(ch.isdigit() for ch in password):
            raise exceptions.ValidationError(detail='Password must contain digit.')
        if not any(ch.isalpha() for ch in password):
            raise exceptions.ValidationError(detail='Password must contain alpha.')
        if len(password) < PASSWORD_LENGTH:
            raise exceptions.ValidationError(detail='Password must be more than 8 character.')

