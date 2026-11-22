from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth.models import User
from rest_framework import serializers


class CustomRegisterSerializer(RegisterSerializer):
    username = None

    def validate_email(self, email):
        # dj-rest-auth only blocks duplicates whose email is *verified*. Verification
        # is optional here, so without this check a second account can be created
        # with an existing user's email.
        email = super().validate_email(email)
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError('An account with this email already exists.')
        return email

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
        }


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)
