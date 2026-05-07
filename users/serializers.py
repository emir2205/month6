from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import ConfirmationCode
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['birthdate'] = user.birthdate.isoformat() if user.birthdate else None
        return token
class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    birthdate = serializers.DateField(required=False, allow_null=True)

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
        except:
            return email
        raise ValidationError('User already exists!')


class ConfirmUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data['email']
        code = data['code']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        try:
            confirmation = ConfirmationCode.objects.get(user=user)
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError("Код подтверждения не найден")

        if confirmation.code != code:
            raise serializers.ValidationError("Неверный код")

        data['user'] = user
        return data

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.is_active = True
        user.save()
        user.confirmation_code.delete()
        return user
