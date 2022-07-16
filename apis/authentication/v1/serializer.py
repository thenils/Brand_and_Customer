from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from brand.models import Brand
from modules.errors import ERRORS


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message=ERRORS['EMAIL_EXISTS'])]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    as_brand = serializers.CharField(write_only=True, required=False)
    name = serializers.CharField(required=False)
    token = serializers.SerializerMethodField(method_name='get_token')

    class Meta:
        model = User
        fields = (
            'email',
            'name',
            'token',
            'password',
            'as_brand'
        )
        extra_kwargs = {
            'email': {'required': True}
        }

    @staticmethod
    def get_token(obj):
        return Token.objects.get(user=obj).key

    def create(self, validated_data):
        with transaction.atomic():
            validated_data['username'] = self.generate_username(validated_data['email'].split('@')[0].replace('+', ''))
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                is_active=True
            )

            if 'as_brand' in validated_data and validated_data['as_brand'].lower() == 'true':
                if 'name' in validated_data:
                    name = validated_data['name']
                else:
                    name = validated_data['email']
                Brand.objects.create(user=user, name=name)

            user.set_password(validated_data['password'])
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return user

    @staticmethod
    def generate_username(user_name):
        ln = User.objects.filter(username__icontains=user_name).count()
        return f'{user_name}@{ln + 1}' if ln > 0 else user_name


class LoginSerializer(serializers.Serializer):
    email_id = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email_id", None)
        filters = Q(username__iexact=email) | Q(email__iexact=email)
        password = data.get("password", None)
        try:
            user = User.objects.get(filters)
        except User.MultipleObjectsReturned:
            raise serializers.ValidationError(
                ERRORS['NO_USER']
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                ERRORS['NO_USER']
            )
        else:
            if not user.check_password(password):
                user = None
        if user is None:
            raise serializers.ValidationError(
                ERRORS['NO_USER']
            )
        token, created = Token.objects.get_or_create(user=user)

        return {
            'email_id': user.email,
            'token': token.key,
        }
