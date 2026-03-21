from rest_framework import serializers
from .models import User

from django.contrib.auth import authenticate


from django.contrib.auth import get_user_model

User = get_user_model()


from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Normalize email (VERY IMPORTANT)
        email = email.lower()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        # Check password manually
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        # Check if user is active
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        data['user'] = user
        return data

class RegisterSerializer(serializers.ModelSerializer):
    # Password field (write_only means it won't show in response)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'role',
            'location',
            'lead'
        ]

    def validate(self, data):
        """
        Custom validation logic
        """
        role = data.get('role')
        lead = data.get('lead')

        # If role is USER, lead must be provided
        if role == 'USER' and not lead:
            raise serializers.ValidationError("User must have a lead (Admin)")

        # Lead must be ADMIN
        if lead and lead.role != 'ADMIN':
            raise serializers.ValidationError("Lead must be an Admin")

        return data

    def create(self, validated_data):
        """
        Create user with hashed password
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # IMPORTANT: hashes password
        user.save()
        return user