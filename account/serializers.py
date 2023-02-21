from datetime import datetime

from .client import Client
from rest_framework import serializers
from account.models import User, ScanData, UserConnection
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from account.utils import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this becoz we need confirm password field in our Registratin Request
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/' + uid + '/' + token
            print('Password Reset Link', link)
            # Send EMail
            body = 'Click Following Link to Reset Your Password ' + link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            # Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')


class UpdateRegisterUserSerializer(serializers.Serializer):
    user_type = serializers.ChoiceField(choices=[('owner', 'Owner'), ('operator', 'Operator')],
                                        default="operator")
    email = serializers.EmailField(
        max_length=255,
        required=True,
    )

    class Meta:
        model = User
        fields = ['email', 'user_type']

    def validate(self, attrs):
        try:
            email = attrs.get('email')
            user_type = attrs.get('user_type')
            user = User.objects.get(email=email)
            user.user_type = user_type
            user.save()
            return attrs
        except Exception as e:
            raise serializers.ValidationError('Email id is not a valid email')


class UserConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConnection
        fields = ['machine_name', 'mac_address', 'status_active', 'last_status']

    def validate(self, attrs):
        try:
            method = self.context['request'].method
            request_data = dict(self.context['request'].data)
            # Get the user ID from the Bearer token
            user_id = self.context['request'].user.id
            user_instance = User.objects.get(id=user_id)
            request_data['user'] = user_instance
            if method == 'POST':
                # Check if UserConnection already exists
                try:
                    UserConnection.objects.get(user_id=user_instance,
                                               machine_name=request_data['machine_name'],
                                               mac_address=request_data['mac_address'])
                    raise serializers.ValidationError('UserConnection already exists')
                except UserConnection.DoesNotExist:
                    # Create new UserConnection
                    response = UserConnection.objects.create(**request_data)
                    return response
            elif method == 'PUT':
                is_connection_alive = self.context['request'].data['is_connection_alive']
                user_connection_obj = UserConnection.objects.get(user_id=user_id)
                if is_connection_alive == 'yes':
                    user_connection_obj.status_active = True
                    user_connection_obj.last_status = datetime.now()
                    user_connection_obj.save()
                    return user_connection_obj
                else:
                    user_connection_obj.status_active = False
                    user_connection_obj.save()
                    return user_connection_obj
        except Exception as e:
            raise serializers.ValidationError(e)


class IsScanSerializer(serializers.Serializer):
    is_scan = serializers.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')],
                                      default="yes")


class ScanDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanData
        fields = ['wavelength', 'energy']

    def validate(self, attrs):
        request_data = dict(attrs)
        try:
            user_id = self.context['request'].user.id
            user_connection_instance = UserConnection.objects.get(user_id=user_id)
            request_data['connection_user'] = user_connection_instance
            response = ScanData.objects.create(**request_data)
            return response
        except Exception as e:
            raise serializers.ValidationError(e)
