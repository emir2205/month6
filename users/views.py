from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ConfirmUserSerializer,
    CustomTokenObtainPairSerializer,
    UserAuthSerializer,
    UserCreateSerializer,
)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmationCode
from rest_framework.views import APIView
import random
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class AuthorizationAPIView(APIView):
    serializer_class = UserAuthSerializer

    @swagger_auto_schema(request_body=UserAuthSerializer)
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'key': token.key})
        return Response({'error': 'user credentials are wrong!'}, status=status.HTTP_401_UNAUTHORIZED)


class RegistrationAPIView(APIView):
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(request_body=UserCreateSerializer)
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        phone_number = serializer.validated_data.get('phone_number', '')
        birthdate = serializer.validated_data.get('birthdate')

        user = User.objects.create_user(
            email=email,
            password=password,
            phone_number=phone_number,
            birthdate=birthdate,
            is_active=False,
        )

        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        ConfirmationCode.objects.create(user=user, code=code)

        print(f'Код подтверждения для пользователя {email}: {code}')

        return Response(
            {'user_id': user.id, 'detail': 'Пользователь создан. Проверьте код подтверждения.'},
            status=status.HTTP_201_CREATED
        )


class ConfirmUserAPIView(APIView):
    serializer_class = ConfirmUserSerializer

    @swagger_auto_schema(request_body=ConfirmUserSerializer)
    def post(self, request):
        serializer = ConfirmUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Пользователь подтвержден и активирован"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
