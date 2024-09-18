from rest_framework import serializers
from account_app.models import User, Profile
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'passwords do not match'})

        # validate password security such as len and only numbers and extra
        try:
            password = attrs['password']
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError({'password': list(e)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        return User.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255, required=True)
    new_password = serializers.CharField(max_length=255, required=True)
    confirm_new_password = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({'new_password': 'passwords do not match'})

        # validate password security such as len and only numbers and extra
        try:
            password = attrs['new_password']
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError({'new_password': list(e)})

        return super().validate(attrs)


class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExists:
            raise serializers.ValidationError({'details': 'email not found'})

        if user.is_verified:
            raise serializers.ValidationError({'details': 'user is already verified'})

        attrs['user'] = user
        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'image', 'description']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({'details': 'user is not verified'})
        validated_data['email'] = self.user.email
        validated_data['user_id'] = self.user.id
        return validated_data

# authtoken

# class CustomAuthTokenSerializer(serializers.Serializer):
#     email = serializers.CharField(
#         label=_("Email"),
#         write_only=True
#     )
#     password = serializers.CharField(
#         label=_("Password"),
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#         write_only=True
#     )
#     token = serializers.CharField(
#         label=_("Token"),
#         read_only=True
#     )
#
#     def validate(self, attrs):
#         username = attrs.get('email')
#         password = attrs.get('password')
#
#         if username and password:
#             user = authenticate(request=self.context.get('request'),
#                                 username=username, password=password)
#
#             # The authenticate call simply returns None for is_active=False
#             # users. (Assuming the default ModelBackend authentication
#             # backend.)
#             if not user:
#                 msg = _('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = _('Must include "username" and "password".')
#             raise serializers.ValidationError(msg, code='authorization')
#
#         attrs['user'] = user
#         return attrs
