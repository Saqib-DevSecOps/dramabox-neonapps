from rest_framework import serializers
from src.services.users.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializes user data for API responses.
    Includes fields for primary key, email, username, first name, and last name.
    The primary key and email are read-only.
    """
    class Meta:
        model = User
        fields = [
            'pk', 'email', 'username', 'first_name', 'last_name'
        ]
        read_only_fields = ['pk', 'email']


class PasswordSerializer(serializers.Serializer):
    """
    Serializes the password for user authentication.
    The password field is required and write-only.
    """
    password = serializers.CharField(required=True, write_only=True)
